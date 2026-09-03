import hashlib
import hmac


class IdentityService:
    """
    Generates purpose-specific pseudonymous identifiers
    without exposing the raw internal user ID to downstream services.
    """

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode("utf-8")

    def generate_pseudonymous_id(
        self,
        internal_user_id: str,
        purpose: str
    ) -> str:

        message = f"{purpose}:{internal_user_id}".encode("utf-8")

        digest = hmac.new(
            self.secret_key,
            message,
            hashlib.sha256
        ).hexdigest()

        return f"{purpose}_{digest[:24]}"