from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.consent import ConsentRecord, ConsentDecision
from app.services.consent_service import consent_service
from app.security.auth import require_api_key


router = APIRouter(
    prefix="/v1/consent",
    tags=["Consent"]
)


@router.post(
    "/set",
    response_model=ConsentDecision,
    dependencies=[Depends(require_api_key)]
)
def set_consent(
    record: ConsentRecord,
    db: Session = Depends(get_db)
):
    consent = consent_service.set_consent(
        db=db,
        internal_user_id=record.internal_user_id,
        purpose=record.purpose.value,
        granted=record.granted,
        source=record.source,
        policy_version=record.policy_version
    )

    return ConsentDecision(
        internal_user_id=consent.internal_user_id,
        purpose=consent.purpose,
        granted=consent.granted,
        source=consent.source,
        policy_version=consent.policy_version,
        created_at=consent.created_at,
        updated_at=consent.updated_at
    )