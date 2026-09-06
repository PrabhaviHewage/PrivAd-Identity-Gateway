import os

from fastapi import Header, HTTPException, status
from dotenv import load_dotenv


load_dotenv()


def require_api_key(
    x_api_key: str | None = Header(default=None)
) -> str:
    expected_api_key = os.getenv("PRIVAD_API_KEY")

    if not expected_api_key:
        raise RuntimeError(
            "PRIVAD_API_KEY is not configured"
        )

    if not x_api_key or x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    return x_api_key