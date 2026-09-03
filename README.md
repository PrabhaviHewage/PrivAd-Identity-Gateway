# PrivAd Identity Gateway

**A privacy-preserving identity and policy enforcement gateway for advertising systems.**

PrivAd Identity Gateway is a privacy engineering project designed to explore how advertising platforms can make identity-processing decisions while applying privacy-by-design principles such as purpose limitation, consent enforcement, pseudonymization, data minimization, policy-based access decisions, and auditable processing.

The system sits between an internal identity source and downstream advertising services, determining whether an identity request should be permitted before issuing a purpose-scoped pseudonymous identifier.

---

## Why This Project Exists

Advertising systems frequently need identity signals for use cases such as:

- advertising
- measurement
- analytics
- personalization

At the same time, identity processing can create significant privacy risks when identifiers are reused across purposes, privacy choices are ignored, or downstream systems receive more identifying information than necessary.

PrivAd Identity Gateway explores an alternative architecture:

> **Evaluate the privacy conditions first, then release only the identity signal required for the permitted purpose.**

Instead of exposing a raw internal user identifier to downstream advertising services, the gateway evaluates the request and, when permitted, generates a purpose-scoped pseudonymous identifier.

---

## Architecture

```text
                    Identity Request
                          |
                          v
                  Purpose Validation
                          |
                          v
                    Consent Lookup
                          |
                          v
                 Privacy Policy Engine
                 /        |         \
                /         |          \
             ALLOW     RESTRICT      DENY
               |
               v
       Purpose-Scoped HMAC
          Pseudonymization
               |
               v
       Pseudonymous Identity
               |
               v
      Downstream Ads Service

Privacy-relevant identity decisions
             |
             v
     Privacy-Safe Audit Log
```

---

## Implemented Privacy Controls

### Purpose Limitation

Identity requests are restricted to explicitly defined processing purposes:

- `advertising`
- `analytics`
- `measurement`
- `personalization`

Unexpected purposes are rejected through request validation.

---

### Purpose-Scoped Pseudonymization

The gateway does not return the raw internal account identifier to downstream services.

Instead, it derives a pseudonymous identifier using HMAC-SHA256 and the requested processing purpose.

Conceptually:

```text
internal_user_id
        +
     purpose
        +
    secret key
        |
        v
HMAC-SHA256
        |
        v
purpose-scoped pseudonymous ID
```

This reduces direct identifier exposure and helps prevent the same downstream identifier from being reused indiscriminately across different purposes.

> Pseudonymization is not anonymization. These identifiers should still be treated as potentially personal data where linkability or re-identification remains possible.

---

### Persistent Consent Enforcement

Consent decisions are persisted using SQLite rather than being held only in application memory.

The gateway checks the stored privacy choice before making an identity decision.

The prototype supports:

- consent grant
- consent withdrawal
- purpose-specific consent
- persistent consent records
- consent update tracking

A withdrawn consent decision affects subsequent identity requests.

---

### Consent Provenance

Consent records include additional context describing the decision:

```text
purpose
granted
source
policy_version
created_at
updated_at
```

This allows the system to retain information about when a privacy choice was recorded, where it originated, and which policy or notice version was associated with it.

---

### Privacy-Safe Audit Logging

Identity decisions are recorded for accountability and debugging.

Audit events capture information such as:

```text
timestamp
event_type
privacy-safe subject identifier
purpose
decision
reason
```

The audit trail intentionally avoids directly logging the raw internal user identifier.

Example:

```json
{
  "event_type": "IDENTITY_REQUEST",
  "subject_id": "subject_9fe1be4249f897df",
  "purpose": "advertising",
  "decision": "DENY",
  "reason": "consent_not_granted"
}
```

---

### Policy Decision Layer

The project includes a prototype policy engine capable of evaluating privacy-relevant request context such as:

```text
region
age group
processing purpose
consent status
```

The policy model supports three decision states:

```text
ALLOW
RESTRICT
DENY
```

The policy rules are prototype engineering rules and should not be interpreted as authoritative implementations of GDPR, UK GDPR, U.S. state privacy laws, or other legal requirements.

---

## Example Identity Request

```json
{
  "internal_user_id": "user_6001",
  "purpose": "advertising",
  "region": "US",
  "age_group": "adult"
}
```

A permitted request can produce a response similar to:

```json
{
  "pseudonymous_id": "advertising_187d678161c14d1c2eb529e2",
  "purpose": "advertising"
}
```

The downstream advertising service therefore receives the pseudonymous identifier rather than the original internal account identifier.

---

## Consent Example

```json
{
  "internal_user_id": "user_6001",
  "purpose": "advertising",
  "granted": true,
  "source": "web",
  "policy_version": "v1.1"
}
```

The persisted record also tracks creation and update timestamps.

---

## API Endpoints

### Health

```http
GET /health
```

### Set or Update Consent

```http
POST /v1/consent/set
```

### Request Pseudonymous Identity

```http
POST /v1/identity/pseudonymize
```

### View Prototype Audit Events

```http
GET /v1/audit/events
```

Interactive API documentation is available through FastAPI Swagger UI while the application is running:

```text
http://127.0.0.1:8000/docs
```

---

## Technology Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- HMAC-SHA256
- Uvicorn
- REST APIs

---

## Privacy Engineering Principles Demonstrated

This project is designed around several privacy engineering concepts:

**Data Minimization**  
Downstream services do not need to receive the raw internal account identifier.

**Purpose Limitation**  
Identity generation is tied to an explicitly declared processing purpose.

**Privacy Choice Enforcement**  
Stored privacy choices influence whether identity processing is permitted.

**Pseudonymization**  
Purpose-scoped identifiers reduce direct exposure of internal identities.

**Accountability**  
Privacy-relevant decisions generate auditable events.

**Policy Enforcement**  
Identity release occurs after policy evaluation rather than being treated as an unconditional operation.

**Privacy by Design**  
Privacy controls are incorporated into the identity architecture itself rather than added only at the interface layer.

---

## Security and Privacy Considerations

This repository is currently an engineering prototype rather than a production identity platform.

Production deployment would require additional controls including:

- managed secrets and key management
- HMAC key rotation and versioning
- API authentication and authorization
- production-grade database infrastructure
- encrypted transport and storage
- rate limiting
- structured security monitoring
- audit-log integrity protection
- retention and deletion policies
- consent history rather than only current-state storage
- formal threat modeling
- formal jurisdiction and lawful-basis policy mapping

Local development secrets and database files are intentionally excluded from version control.

---

## Current Development Focus

The current development phase is extending the gateway from consent-aware identity processing toward contextual privacy policy enforcement.

Areas under development include:

- regional privacy policy evaluation
- age-aware advertising restrictions
- richer policy decision explanations
- automated testing
- privacy threat modeling
- stronger audit controls
- policy configuration and versioning

---

## Project Goal

PrivAd Identity Gateway is a portfolio and research-oriented privacy engineering project exploring a broader question:

> **How can identity infrastructure support advertising functionality while technically enforcing privacy choices, purpose boundaries, and data minimization before identity data reaches downstream systems?**

The project is being developed iteratively, with privacy requirements treated as enforceable system behavior rather than documentation alone.

---

## Author

**Prabhavi Hewage**

Privacy Engineering | Privacy Technology | Cybersecurity & GRC

GitHub: `PrabhaviHewage`