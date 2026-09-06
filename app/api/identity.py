from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.identity import IdentityRequest, IdentityResponse
from app.models.policy import PolicyAction
from app.services.audit_service import audit_service
from app.services.consent_service import consent_service
from app.services.identity_service import IdentityService
from app.services.policy_service import policy_service
from app.services.policy_service import policy_service
from app.services.policy_service import policy_service
from app.services.policy_service import policy_service
from app.services.identity_service import identity_service


router = APIRouter(
    prefix="/v1/identity",
    tags=["Identity"]
)


@router.post(
    "/pseudonymize",
    response_model=IdentityResponse
)
def pseudonymize_identity(
    request: IdentityRequest,
    db: Session = Depends(get_db)
):

    purpose = request.purpose.value

    has_consent = consent_service.has_consent(
        db=db,
        internal_user_id=request.internal_user_id,
        purpose=purpose
    )

    policy_result = policy_service.evaluate(
        region=request.region.value,
        age_group=request.age_group.value,
        purpose=purpose,
        has_consent=has_consent
    )

    if policy_result.decision.value != "ALLOW":

        audit_service.log_event(
            internal_user_id=request.internal_user_id,
            event_type="IDENTITY_REQUEST",
            purpose=purpose,
            decision=policy_result.decision.value,
            reason=policy_result.reason
        )

        raise HTTPException(
            status_code=403,
            detail={
                "decision": policy_result.decision.value,
                "reason": policy_result.reason,
                "purpose": purpose,
                "region": request.region.value,
                "age_group": request.age_group.value
            }
        )

    pseudonymous_id, key_version = (
    identity_service.generate_pseudonymous_id(
        internal_user_id=request.internal_user_id,
        purpose=purpose
    )
)

    audit_service.log_event(
        internal_user_id=request.internal_user_id,
        event_type="IDENTITY_REQUEST",
        purpose=purpose,
        decision="ALLOW",
        reason=policy_result.reason
    )

    return IdentityResponse(
        pseudonymous_id=pseudonymous_id,
        purpose=request.purpose
    )