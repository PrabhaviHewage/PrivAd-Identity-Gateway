from fastapi import FastAPI

from app.api.identity import router as identity_router
from app.api.consent import router as consent_router

from app.api.audit import router as audit_router
from app.database.database import Base, engine
from app.database import consent_model



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PrivAd Identity Gateway",
    description=(
        "Privacy-preserving identity and audience eligibility gateway "
        "for advertising platforms."
    ),
    version="0.3.0",
)


app.include_router(identity_router)
app.include_router(consent_router)
app.include_router(audit_router)

@app.get("/")
def root():
    return {
        "service": "PrivAd Identity Gateway",
        "version": "0.3.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }