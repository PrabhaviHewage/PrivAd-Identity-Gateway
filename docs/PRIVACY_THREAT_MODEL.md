# PrivAd Identity Gateway — Privacy Threat Model

## 1. Purpose

This document identifies privacy and security threats associated with the PrivAd Identity Gateway and describes the controls implemented or proposed to mitigate those risks.

The gateway is designed to mediate identity access between internal account systems and downstream advertising services. Its primary privacy objective is to prevent identity information from being released without appropriate purpose, consent, and policy evaluation.

This threat model focuses particularly on risks involving identity, advertising, consent, pseudonymization, policy enforcement, and auditability.

---

## 2. System Context

The simplified data flow is:

```text
Internal Identity
       |
       v
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
       |
       +----------+----------+
       |          |          |
     ALLOW     RESTRICT     DENY
       |
       v
Purpose-Scoped
Pseudonymization
       |
       v
Downstream Advertising Service

Privacy-Relevant Decisions
       |
       v
Privacy-Safe Audit Log
```

The gateway acts as a privacy enforcement boundary between identifiable account data and advertising systems.

---

## 3. Sensitive Assets

The system handles or protects several privacy-relevant assets.

### Internal User Identifier

The internal account identifier represents the original identity used by the platform.

Example:

```text
user_7001
```

Exposure of this identifier to unnecessary downstream systems could increase linkability and identity disclosure risk.

### Pseudonymous Advertising Identifier

A purpose-scoped identifier generated using HMAC-SHA256.

Example:

```text
advertising_a81f...
```

Although pseudonymous, this value may still constitute personal data where it can be linked to an individual or other information.

### Consent Records

Consent records include:

```text
internal_user_id
purpose
granted
source
policy_version
created_at
updated_at
```

Unauthorized modification of these records could change whether identity processing is permitted.

### HMAC Secret

The HMAC secret protects the derivation of pseudonymous identifiers.

Compromise of this key could weaken the security properties of the pseudonymization mechanism.

### Privacy Policy Decisions

Policy decisions determine whether identity processing results in:

```text
ALLOW
RESTRICT
DENY
```

Manipulation or bypass of these decisions could result in processing inconsistent with configured privacy rules.

### Audit Records

Audit events provide evidence of privacy-relevant identity decisions.

Loss or manipulation of these records could reduce accountability and make misuse more difficult to detect.

---

## 4. Trust Boundaries

The architecture contains several important trust boundaries.

### Boundary 1 — Client to Identity Gateway

Requests entering the API cannot automatically be trusted.

Potential risks include:

- forged identity requests
- manipulated purpose values
- manipulated regional context
- manipulated age information
- excessive request volume

### Boundary 2 — Gateway to Consent Store

The gateway relies on stored consent information when evaluating identity requests.

Unauthorized database changes could result in incorrect policy decisions.

### Boundary 3 — Gateway to Downstream Advertising Systems

Only the minimum identity signal required for an approved purpose should cross this boundary.

Raw internal identifiers should not be unnecessarily disclosed.

### Boundary 4 — Application to Audit System

Audit information must provide accountability without creating a secondary repository of unnecessary identity information.

---

## 5. Threat Analysis

| ID | Threat | Privacy Impact | Current Control | Residual / Future Work |
|---|---|---|---|---|
| T01 | Raw internal identifier exposed to downstream advertising services | Identity disclosure and increased linkability | Gateway returns purpose-scoped pseudonymous IDs | Add integration tests ensuring raw IDs never appear in downstream responses |
| T02 | Identifier reused across different purposes | Cross-purpose profiling and purpose limitation failure | Purpose is incorporated into HMAC derivation | Add explicit unlinkability tests across purposes |
| T03 | Identity issued after consent withdrawal | Processing contrary to stored privacy choice | Consent checked before identity issuance | Maintain consent history and distributed revocation propagation |
| T04 | Invalid processing purpose submitted | Unauthorized or undefined processing | Pydantic enum restricts supported purposes | Move purpose definitions to centrally versioned policy configuration |
| T05 | Minor receives advertising identity | Increased risk involving younger users | Prototype age-aware policy returns DENY | Add trustworthy age-signal architecture and jurisdiction-specific rules |
| T06 | Regional privacy rule bypassed | Processing inconsistent with configured regional policy | Policy engine evaluates region | Region should come from a trusted signal rather than unverified client input |
| T07 | HMAC secret compromised | Identifier derivation could be reproduced by unauthorized parties | Secret stored outside source code in local `.env` | Use managed KMS/secret manager, rotation and key versioning |
| T08 | Consent database modified without authorization | False consent state and unauthorized identity processing | Persistent database-backed consent lookup | Add authentication, authorization and database access controls |
| T09 | Audit log contains raw identifiers | Audit infrastructure becomes an additional privacy risk | Audit records use privacy-safe subject identifiers | Replace simple hashing with keyed pseudonymization and define retention |
| T10 | Audit records altered or deleted | Loss of accountability and incident evidence | Audit events currently recorded | Add append-only/tamper-evident audit storage |
| T11 | Policy engine bypassed | Identity could be generated without privacy evaluation | Identity endpoint invokes policy evaluation before pseudonymization | Architect policy enforcement as a mandatory centralized boundary |
| T12 | Client falsifies age group | Advertising processing may be incorrectly permitted | Age-aware rules exist | Do not trust self-declared API fields in production; use trusted age/eligibility signals |
| T13 | Client falsifies region | Incorrect jurisdictional policy may execute | Region enum and policy evaluation | Derive region from an authoritative service or trusted context |
| T14 | Excessive identity requests enable enumeration or abuse | Profiling, identifier harvesting, operational abuse | Not yet implemented | Add authentication, authorization, rate limiting and anomaly detection |
| T15 | Pseudonymous identifiers retained indefinitely | Long-term linkability increases privacy risk | Purpose separation limits some reuse | Define identifier lifecycle, retention and rotation policies |
| T16 | Consent provenance overwritten | Historical evidence of privacy choices may be lost | Current record stores timestamps and policy version | Add immutable consent history/event records |

---

## 6. Privacy Abuse Cases

### Abuse Case A — Cross-Purpose Tracking

An advertising service attempts to obtain identifiers for several purposes and correlate them.

**Risk:** creation of a broader behavioral profile than intended.

**Current mitigation:** the processing purpose participates in pseudonymous identifier derivation.

**Future control:** enforce downstream audience boundaries and test that identifiers generated for separate purposes cannot be trivially reused as a common identifier.

---

### Abuse Case B — Processing After Withdrawal

A user grants advertising consent and later withdraws it.

A downstream service subsequently requests another advertising identifier.

**Expected behavior:** the gateway reevaluates the current privacy choice and prevents unrestricted identity issuance.

Automated tests verify the withdrawal behavior.

---

### Abuse Case C — Minor Advertising Request

A request identifies the subject as a minor while requesting an advertising identity.

**Expected behavior:**

```text
DENY
```

The decision is also recorded in the privacy audit trail.

---

### Abuse Case D — Unknown Processing Purpose

A client submits:

```json
{
  "purpose": "steal_data"
}
```

The request is rejected by schema validation because the purpose is outside the defined purpose allowlist.

---

### Abuse Case E — Audit Database Becomes an Identity Dataset

A system may implement extensive auditing for accountability but accidentally log every raw internal identifier.

This creates a new repository of identity information.

PrivAd currently reduces this risk by generating a separate privacy-safe subject identifier for audit events rather than directly recording the raw internal identifier.

---

## 7. Important Residual Risk: Audit Identifier Construction

The prototype currently derives the audit `subject_id` using SHA-256 over the internal identifier.

This removes the raw identifier from the log but is not sufficient protection for production environments when source identifiers are predictable.

For example, identifiers such as:

```text
user_1
user_2
user_3
```

could potentially be guessed and hashed offline.

A stronger design would use a separate keyed HMAC specifically for audit pseudonymization:

```text
audit_subject_id =
HMAC(audit_key, internal_user_id)
```

The audit key should be separated from the advertising identity pseudonymization key.

This provides domain separation and reduces straightforward dictionary attacks against predictable identifiers.

---

## 8. Security and Privacy Controls Roadmap

The following controls would strengthen the prototype:

- API authentication
- role-based authorization
- managed secret storage
- HMAC key rotation
- separate keys by cryptographic purpose
- consent history
- policy versioning
- trusted regional signals
- trusted age/eligibility signals
- rate limiting
- abuse detection
- audit retention rules
- tamper-evident audit storage
- identifier expiration and rotation
- automated privacy regression tests
- structured policy configuration

---

## 9. Privacy Invariants

The system should maintain the following engineering invariants.

### Invariant 1

A raw internal user identifier must not be returned as the advertising identity.

### Invariant 2

An identity request must be evaluated against a defined processing purpose.

### Invariant 3

Privacy policy evaluation must occur before a pseudonymous advertising identity is released.

### Invariant 4

Withdrawal of the relevant privacy permission must affect subsequent identity decisions.

### Invariant 5

A minor advertising request must not receive an advertising identity under the current prototype policy.

### Invariant 6

Privacy audit events should not directly contain the raw internal account identifier.

### Invariant 7

Different processing purposes should produce different pseudonymous identifiers for the same internal identity.

---

## 10. Threat Modeling Status

This document represents the current threat model for the prototype and will evolve alongside the system.

Implemented controls are distinguished from future controls so that the threat model does not imply production-level protections that have not yet been implemented.

The objective is to continuously translate identified privacy risks into technical controls and automated privacy tests.