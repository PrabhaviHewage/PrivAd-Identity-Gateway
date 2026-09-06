from fastapi import APIRouter, Depends

from app.security.auth import require_api_key
from app.services.audit_service import audit_service
from app.security.auth import require_role

router = APIRouter(
    prefix="/v1/audit",
    tags=["Audit"]
)


@router.get(
    "/events",
    dependencies=[Depends(require_role("privacy_admin"))]
)
def get_audit_events():
    return {"events": audit_service.get_events()}