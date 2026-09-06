import hashlib
import hmac

from app.security.key_manager import key_manager


class IdentityService:
    """
    Generates purpose-scoped pseudonymous identifiers
    using the currently active versioned HMAC key.
    """

    def generate_pseudonymous_id(
        self,
        internal_user_id: str,
        purpose: str
    ) -> tuple[str, str]:

        key_version, secret_key = key_manager.get_active_key()

        message = f"{purpose}:{internal_user_id}".encode("utf-8")

        digest = hmac.new(
            secret_key.encode("utf-8"),
            message,
            hashlib.sha256
        ).hexdigest()

        pseudonymous_id = (
            f"{purpose}_{key_version}_{digest[:24]}"
        )

        return pseudonymous_id, key_version


identity_service = IdentityService()