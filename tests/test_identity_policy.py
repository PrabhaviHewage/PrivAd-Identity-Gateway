from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def set_consent(
    internal_user_id: str,
    purpose: str,
    granted: bool
):
    return client.post(
        "/v1/consent/set",
        json={
            "internal_user_id": internal_user_id,
            "purpose": purpose,
            "granted": granted,
            "source": "pytest",
            "policy_version": "test-v1"
        }
    )


def test_adult_with_consent_is_allowed():
    set_consent(
        internal_user_id="test_user_allow",
        purpose="advertising",
        granted=True
    )

    response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_allow",
            "purpose": "advertising",
            "region": "US",
            "age_group": "adult"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["purpose"] == "advertising"
    assert data["pseudonymous_id"].startswith(
        "advertising_"
    )


def test_minor_is_denied():
    set_consent(
        internal_user_id="test_user_minor",
        purpose="advertising",
        granted=True
    )

    response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_minor",
            "purpose": "advertising",
            "region": "US",
            "age_group": "minor"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"]["decision"] == "DENY"


def test_no_consent_is_restricted():
    response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_no_consent",
            "purpose": "advertising",
            "region": "US",
            "age_group": "adult"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"]["decision"] == "RESTRICT"


def test_invalid_purpose_is_rejected():
    response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_invalid",
            "purpose": "steal_data",
            "region": "US",
            "age_group": "adult"
        }
    )

    assert response.status_code == 422


def test_consent_withdrawal_blocks_identity():
    set_consent(
        internal_user_id="test_user_withdrawal",
        purpose="advertising",
        granted=True
    )

    allowed_response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_withdrawal",
            "purpose": "advertising",
            "region": "US",
            "age_group": "adult"
        }
    )

    assert allowed_response.status_code == 200

    set_consent(
        internal_user_id="test_user_withdrawal",
        purpose="advertising",
        granted=False
    )

    denied_response = client.post(
        "/v1/identity/pseudonymize",
        json={
            "internal_user_id": "test_user_withdrawal",
            "purpose": "advertising",
            "region": "US",
            "age_group": "adult"
        }
    )

    assert denied_response.status_code == 403

    data = denied_response.json()

    assert data["detail"]["decision"] == "RESTRICT"