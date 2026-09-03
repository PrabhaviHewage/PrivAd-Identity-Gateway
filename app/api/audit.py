from fastapi import APIRouter

from app.services.audit_service import audit_service


router = APIRouter(
    prefix="/v1/audit",
    tags=["Audit"]
)


@router.get("/events")
def get_audit_events():
    return {
        "events": audit_service.get_events()
    }