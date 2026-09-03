from enum import Enum

from pydantic import BaseModel


class PolicyAction(str, Enum):
    ALLOW = "ALLOW"
    RESTRICT = "RESTRICT"
    DENY = "DENY"


class PolicyResponse(BaseModel):
    action: PolicyAction
    reason: str
    mode: str