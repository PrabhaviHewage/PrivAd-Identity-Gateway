import os

from dotenv import load_dotenv


load_dotenv()


class KeyManager:
    """
    Prototype key manager for identity pseudonymization.

    Supports explicit key versioning so generated identifiers can
    record which HMAC key version was used.
    """

    def __init__(self):
        self.active_version = os.getenv(
            "PRIVAD_ACTIVE_KEY_VERSION",
            "v1"
        )

        self.keys = {
            "v1": os.getenv("PRIVAD_SECRET_KEY_V1"),
            "v2": os.getenv("PRIVAD_SECRET_KEY_V2"),
        }

        active_key = self.keys.get(self.active_version)

        if not active_key:
            raise RuntimeError(
                f"No key configured for active version "
                f"{self.active_version}"
            )

    def get_active_key(self) -> tuple[str, str]:
        return (
            self.active_version,
            self.keys[self.active_version]
        )

    def get_key(self, version: str) -> str:
        key = self.keys.get(version)

        if not key:
            raise KeyError(
                f"Unknown or unavailable key version: {version}"
            )

        return key


key_manager = KeyManager()