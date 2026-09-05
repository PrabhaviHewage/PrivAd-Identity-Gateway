import hashlib
import hmac
import os
from datetime import datetime, timezone

from dotenv import load_dotenv


load_dotenv()


class AuditService:
    """
    Privacy-safe in-memory audit logger for the PrivAd prototype.

    Raw internal user identifiers are not stored directly.
    A dedicated HMAC key is used for audit subject pseudonymization.
    """

    def __init__(self):
        audit_secret = os.getenv("PRIVAD_AUDIT_SECRET_KEY")

        if not audit_secret:
            raise RuntimeError(
                "PRIVAD_AUDIT_SECRET_KEY is not configured"
            )

        self.audit_secret = audit_secret.encode("utf-8")
        self._events = []

    def _privacy_safe_subject_id(
        self,
        internal_user_id: str
    ) -> str:

        message = f"audit:{internal_user_id}".encode("utf-8")

        digest = hmac.new(
            self.audit_secret,
            message,
            hashlib.sha256
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