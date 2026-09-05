from dataclasses import dataclass
from enum import Enum


class PolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    RESTRICT = "RESTRICT"


@dataclass
class PolicyResult:
    decision: PolicyDecision
    reason: str


class PolicyService:
    """
    Prototype privacy policy engine for advertising identity decisions.
    """

    def evaluate(
        self,
        region: str,
        age_group: str,
        purpose: str,
        has_consent: bool
    ) -> PolicyResult:

        normalized_region = region.upper()
        normalized_age_group = age_group.lower()

        # Minors are denied advertising identity processing
        # under this prototype policy.
        if (
            normalized_age_group == "minor"
            and purpose == "advertising"
        ):
            return PolicyResult(
                decision=PolicyDecision.DENY,
                reason="Advertising identity is not permitted for minors."
            )

        # Prototype EU/EEA/UK advertising rule.
        if normalized_region in {"EU", "EEA", "UK"}:
            if purpose == "advertising" and not has_consent:
                return PolicyResult(
                    decision=PolicyDecision.DENY,
                    reason=(
                        "Advertising identity requires an affirmative "
                        "privacy choice under this prototype policy."
                    )
                )

        # Other regions without consent receive a restricted decision.
        if purpose == "advertising" and not has_consent:
            return PolicyResult(
                decision=PolicyDecision.RESTRICT,
                reason=(
                    "Advertising identity is restricted because "
                    "consent is not available."
                )
            )

        return PolicyResult(
            decision=PolicyDecision.ALLOW,
            reason="Request satisfies the current prototype policy."
        )


policy_service = PolicyService()