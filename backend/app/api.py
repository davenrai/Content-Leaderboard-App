from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas, models, crud
from auth import get_current_user_optional, get_current_user, create_access_token
from database import get_db

router = APIRouter(prefix="/api")


@router.get("/")
async def root():
    return {"message": "Knotch Take Home Challenge by Daven Boparai"}


@router.get("/content", response_model=schemas.ContentListResponse, tags=["Content"])
def get_content_list(
    cursor: str | None = None,
    limit: int = 10,
    search: str | None = None,
    sort_field: schemas.SortField | None = schemas.SortField.title,
    sort_order: schemas.SortOrder | None = schemas.SortOrder.desc,
    db: Session = Depends(get_db),
    current_user: Annotated[
        models.User | None, Depends(get_current_user_optional)
    ] = None,
):
    """
    Get content with cursor pagination. (For better performance in a large leaderboard table.)
    """
    # Decode cursor if provided
    cursor_data = None
    if cursor:
        cursor_data = crud.decode_cursor(cursor)
        if cursor_data is None:
            raise HTTPException(status_code=400, detail="Invalid cursor")

    # Get items with cursor pagination
    items, next_cursor_data = crud.get_content_list_cursor(
        db,
        cursor_data=cursor_data,
        limit=limit,
        search=search,
        sort_field=sort_field,
        sort_order=sort_order,
    )

    # Encode next cursor
    next_cursor = None
    if next_cursor_data:
        next_cursor = crud.encode_cursor(next_cursor_data)

    return schemas.ContentListResponse(
        items=items,
        next_cursor=next_cursor,
        total=len(items),
        has_more=next_cursor is not None,
    )


@router.post("/content", response_model=schemas.Content, tags=["Content"])
def create_content(
    content: schemas.ContentCreate,
    db: Session = Depends(get_db),
    current_user: Annotated[
        models.User | None, Depends(get_current_user_optional)
    ] = None,
):
    if current_user:
        print(f"User {current_user.username} creating content")
    try:
        return crud.create_content(db=db, content=content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/content/{content_id}", response_model=schemas.Content, tags=["Content"])
def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    content = crud.get_content(db=db, content_id=content_id)
    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find content with ID: {content_id}",
        )
    return content


@router.delete("/content/{content_id}", tags=["Content"])
def delete_content(
    content_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_content = crud.delete_content(db, content_id=content_id)
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )
    return {"message": "Content successfully deleted"}


@router.put("/content/{content_id}", tags=["Content"])
def update_content(
    content_id: int,
    content: schemas.ContentUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    database_content = crud.update_content(db, content_id=content_id, content=content)
    if database_content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )
    return database_content


@router.post("/register", response_model=schemas.User, tags=["Authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return crud.create_user(db=db, user=user)


@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """Login to get access token."""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User, tags=["Authentication"])
def get_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user
