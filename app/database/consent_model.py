from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)

from app.database.database import Base


class ConsentDB(Base):
    __tablename__ = "consents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    internal_user_id = Column(
        String,
        nullable=False,
        index=True
    )

    purpose = Column(
        String,
        nullable=False
    )

    granted = Column(
        Boolean,
        nullable=False
    )

    source = Column(
        String,
        nullable=False,
        default="api"
    )

    policy_version = Column(
        String,
        nullable=False,
        default="v1.0"
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "internal_user_id",
            "purpose",
            name="uq_user_purpose"
        ),
    )