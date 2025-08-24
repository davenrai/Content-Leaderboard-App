from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from pydantic import BaseModel, AfterValidator, ConfigDict


def is_scroll_depth_valid(value: float) -> float:
    if not 0.0 <= value <= 100.0:
        raise ValueError(
            f"value of scroll depth must be between 0.0 and 100.0, got {value}"
        )
    return value


def validate_non_negative(value: int | None) -> int | None:
    if value is not None and value < 0:
        raise ValueError("Count values must be non-negative")
    return value


def validate_publish_date(pub_date: datetime) -> datetime:
    min_date = datetime(1990, 1, 1)
    max_date = datetime.now()
    if not (min_date <= pub_date <= max_date):
        raise ValueError(
            f"publish_date must be between {min_date.date()} and {max_date.date()}"
        )
    return pub_date


class ContentItem(BaseModel):
    title: str
    url: str
    publish_date: Annotated[datetime, AfterValidator(validate_publish_date)]
    page_view_count: Annotated[int, AfterValidator(validate_non_negative)] = 0
    click_count: Annotated[int, AfterValidator(validate_non_negative)] = 0
    conversion_count: Annotated[int, AfterValidator(validate_non_negative)] = 0
    average_scroll_depth: Annotated[float, AfterValidator(is_scroll_depth_valid)] = 0.0


class Content(ContentItem):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentListResponse(BaseModel):
    items: List[Content]
    next_cursor: Optional[str] = None
    has_more: bool
    total: Optional[int] = None  # Optional for cursor pagination


class ContentCreate(ContentItem):
    pass


class ContentUpdate(ContentItem):
    title: str | None = None
    url: str | None = None
    publish_date: Annotated[datetime, AfterValidator(validate_publish_date)] | None = (
        None
    )
    page_view_count: Annotated[int, AfterValidator(validate_non_negative)] | None = None
    click_count: Annotated[int, AfterValidator(validate_non_negative)] | None = None
    conversion_count: Annotated[int, AfterValidator(validate_non_negative)] | None = (
        None
    )
    average_scroll_depth: (
        Annotated[float, AfterValidator(is_scroll_depth_valid)] | None
    ) = None


class SortField(str, Enum):
    title = "title"
    publish_date = "publish_date"
    # More can be added here


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
