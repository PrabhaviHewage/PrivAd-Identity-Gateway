import hashlib
from datetime import datetime, timezone


class AuditService:
    """
    Privacy-safe in-memory audit logger for the PrivAd prototype.

    Raw internal user identifiers are not stored directly.
    """

    def __init__(self):
        self._events = []

    def _privacy_safe_subject_id(
        self,
        internal_user_id: str
    ) -> str:

        digest = hashlib.sha256(
            internal_user_id.encode("utf-8")
        ).hexdigest()

        return f"subject_{digest[:16]}"

    def log_event(
        self,
        internal_user_id: str,
        event_type: str,
        purpose: str,
        decision: str,
        reason: str
    ):
        event = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "event_type": event_type,
            "subject_id": self._privacy_safe_subject_id(
                internal_user_id
            ),
            "purpose": purpose,
            "decision": decision,
            "reason": reason
        }

        self._events.append(event)

        return event

    def get_events(self):
        return self._events


audit_service = AuditService()