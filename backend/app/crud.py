import base64
import json
from datetime import datetime, date
from typing import Optional, Dict, Any, Tuple, List

from passlib.context import CryptContext
from sqlalchemy import or_, desc, asc, select, and_, func
from sqlalchemy.orm import Session
import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_content(db: Session, content_id: int):
    return db.query(models.Content).where(models.Content.id == content_id).first()


# Cursor Utilities
def encode_cursor(data: Dict[str, Any]) -> str:
    """Encode cursor data to base64 string."""
    json_str = json.dumps(data, default=str)
    return base64.b64encode(json_str.encode()).decode()


def decode_cursor(cursor: str) -> Dict[str, Any]:
    """Decode cursor from base64 string."""
    json_str = base64.b64decode(cursor.encode()).decode()
    return json.loads(json_str)


def get_content_list_cursor(
    db: Session,
    cursor_data: Optional[Dict[str, Any]] = None,
    limit: int = 10,
    search: Optional[str] = None,
    sort_field: str = "publish_date",
    sort_order: str = "desc",
) -> Tuple[List[models.Content], Optional[Dict[str, Any]]]:
    query = select(models.Content)

    # Apply search filter
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(
                models.Content.title.ilike(search_filter),
                models.Content.url.ilike(search_filter),
            )
        )

    # Apply cursor filter
    if cursor_data:
        cursor_value = cursor_data.get(sort_field)
        cursor_id = cursor_data.get("id")

        if cursor_value is not None and cursor_id is not None:
            # Handle different field types
            if sort_field == "title":
                # For title, we need case-insensitive comparison
                # cursor_value should already be lowercase from previous iteration
                if sort_order == "desc":
                    query = query.where(
                        or_(
                            func.lower(models.Content.title) < cursor_value,
                            and_(
                                func.lower(models.Content.title) == cursor_value,
                                models.Content.id > cursor_id,
                            ),
                        )
                    )
                else:
                    query = query.where(
                        or_(
                            func.lower(models.Content.title) > cursor_value,
                            and_(
                                func.lower(models.Content.title) == cursor_value,
                                models.Content.id > cursor_id,
                            ),
                        )
                    )
            else:
                # For other fields
                sort_column = getattr(models.Content, sort_field)

                # Convert string dates back to date objects for comparison
                if sort_field == "publish_date" and isinstance(cursor_value, str):
                    cursor_value = datetime.strptime(
                        cursor_value, "%Y-%m-%dT%H:%M:%S"
                    ).date()

                if sort_order == "desc":
                    # For descending: get items less than cursor OR equal with higher ID
                    query = query.where(
                        or_(
                            sort_column < cursor_value,
                            and_(
                                sort_column == cursor_value,
                                models.Content.id > cursor_id,
                            ),
                        )
                    )
                else:
                    # For ascending: get items greater than cursor OR equal with higher ID
                    query = query.where(
                        or_(
                            sort_column > cursor_value,
                            and_(
                                sort_column == cursor_value,
                                models.Content.id > cursor_id,
                            ),
                        )
                    )

    # Apply sorting - must match the cursor comparison logic
    if sort_field == "title":
        # Case-insensitive sorting for title
        if sort_order == "desc":
            query = query.order_by(
                desc(func.lower(models.Content.title)), asc(models.Content.id)
            )
        else:
            query = query.order_by(
                asc(func.lower(models.Content.title)), asc(models.Content.id)
            )
    else:
        # Regular sorting for other fields
        sort_column = getattr(models.Content, sort_field)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column), asc(models.Content.id))
        else:
            query = query.order_by(asc(sort_column), asc(models.Content.id))

    # Get one extra item so we can check if there are more items
    items = db.scalars(query.limit(limit + 1)).all()

    # Check if there are more items
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]  # Remove the extra item

    # Create cursor for next page
    next_cursor_data = None
    if items and has_more:
        last_item = items[-1]

        # Need to handle title (string) differently because of case-insensitive
        # This can be handled differently if other sort_fields were allowed
        if sort_field == "title":
            cursor_value = last_item.title.lower()
        else:
            cursor_value = getattr(last_item, sort_field)

            if isinstance(cursor_value, date):
                cursor_value = cursor_value.isoformat()

        next_cursor_data = {"id": last_item.id, sort_field: cursor_value}

    return items, next_cursor_data


def create_content(db: Session, content: schemas.ContentCreate) -> models.Content:
    database_content = models.Content(**content.model_dump())
    db.add(database_content)
    db.commit()
    db.refresh(database_content)
    return database_content


def delete_content(db: Session, content_id: int) -> int:
    deleted_count = (
        db.query(models.Content).where(models.Content.id == content_id).delete()
    )
    db.commit()
    return deleted_count > 0


def update_content(db: Session, content_id: int, content: schemas.ContentUpdate):
    database_content = get_content(db, content_id)
    if database_content:
        update_data = content.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(database_content, field, value)
        db.commit()
        db.refresh(database_content)
    return database_content


# Users CRUD
def get_user(db: Session, username: str) -> models.User | None:
    return db.scalar(select(models.User).where(models.User.username == username))


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
