from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, Float, Index, func

from database import Base


# Content Item
class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    url = Column(String, index=True, nullable=False, unique=True)
    publish_date = Column(DateTime, default=datetime.now, index=True, nullable=False)
    page_view_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    conversion_count = Column(Integer, default=0)
    average_scroll_depth = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        Index("ix_content_lower_title", func.lower(title)),
        Index("ix_content_lower_url", func.lower(url)),
    )


# User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
