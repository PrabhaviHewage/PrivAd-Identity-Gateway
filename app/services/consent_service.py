from sqlalchemy.orm import Session

from app.database.consent_model import ConsentDB


class ConsentService:
    """
    Persistent consent service backed by SQLite.
    """

    def set_consent(
        self,
        db: Session,
        internal_user_id: str,
        purpose: str,
        granted: bool,
        source: str,
        policy_version: str
    ) -> ConsentDB:

        consent = (
            db.query(ConsentDB)
            .filter(
                ConsentDB.internal_user_id == internal_user_id,
                ConsentDB.purpose == purpose
            )
            .first()
        )

        if consent:
            consent.granted = granted
            consent.source = source
            consent.policy_version = policy_version

        else:
            consent = ConsentDB(
                internal_user_id=internal_user_id,
                purpose=purpose,
                granted=granted,
                source=source,
                policy_version=policy_version
            )

            db.add(consent)

        db.commit()
        db.refresh(consent)

        return consent

    def has_consent(
        self,
        db: Session,
        internal_user_id: str,
        purpose: str
    ) -> bool:

        consent = (
            db.query(ConsentDB)
            .filter(
                ConsentDB.internal_user_id == internal_user_id,
                ConsentDB.purpose == purpose
            )
            .first()
        )

        if not consent:
            return False

        return consent.granted


consent_service = ConsentService()