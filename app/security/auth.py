import os

from fastapi import Header, HTTPException, status
from dotenv import load_dotenv


load_dotenv()


ROLE_KEYS = {
    "identity": os.getenv("PRIVAD_IDENTITY_API_KEY"),
    "consent": os.getenv("PRIVAD_CONSENT_API_KEY"),
    "privacy_admin": os.getenv("PRIVAD_PRIVACY_ADMIN_API_KEY"),
}


def require_role(required_role: str):
    def dependency(
        x_api_key: str | None = Header(default=None)
    ) -> str:
        expected_api_key = ROLE_KEYS.get(required_role)

        if not expected_api_key:
            raise RuntimeError(
                f"API key is not configured for role: {required_role}"
            )

        if not x_api_key or x_api_key != expected_api_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role} access required"
            )

        return required_role

    return dependency