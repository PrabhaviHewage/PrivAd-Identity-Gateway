from datetime import datetime

from pydantic import BaseModel, Field

from app.models.identity import IdentityPurpose


class ConsentRecord(BaseModel):
    internal_user_id: str

    purpose: IdentityPurpose

    granted: bool

    source: str = Field(
        default="api",
        min_length=1,
        description="Where the consent decision was collected"
    )

    policy_version: str = Field(
        default="v1.0",
        min_length=1,
        description="Privacy policy or consent notice version"
    )


class ConsentDecision(BaseModel):
    internal_user_id: str
    purpose: IdentityPurpose
    granted: bool
    source: str
    policy_version: str
    created_at: datetime
    updated_at: datetime