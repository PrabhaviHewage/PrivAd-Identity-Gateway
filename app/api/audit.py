from fastapi import APIRouter, Depends

from app.security.auth import require_api_key
from app.services.audit_service import audit_service


router = APIRouter(
    prefix="/v1/audit",
    tags=["Audit"]
)


@router.get(
    "/events",
    dependencies=[Depends(require_api_key)]
)
def get_audit_events():
    return {"events": audit_service.get_events()}