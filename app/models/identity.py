from enum import Enum

from pydantic import BaseModel, Field


class IdentityPurpose(str, Enum):
    ADVERTISING = "advertising"
    ANALYTICS = "analytics"
    MEASUREMENT = "measurement"
    PERSONALIZATION = "personalization"


class AgeGroup(str, Enum):
    ADULT = "adult"
    MINOR = "minor"


class Region(str, Enum):
    US = "US"
    EU = "EU"
    EEA = "EEA"
    UK = "UK"
    OTHER = "OTHER"


class IdentityRequest(BaseModel):
    internal_user_id: str = Field(
        ...,
        min_length=1,
        description="Internal account identifier"
    )

    purpose: IdentityPurpose

    region: Region = Region.OTHER

    age_group: AgeGroup = AgeGroup.ADULT


class IdentityResponse(BaseModel):
    pseudonymous_id: str
    purpose: IdentityPurpose