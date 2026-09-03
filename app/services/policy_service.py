from app.models.policy import PolicyAction, PolicyResponse


class PolicyService:
    """
    Prototype policy engine for privacy-aware
    advertising identity decisions.
    """

    def evaluate(
        self,
        region: str,
        age_group: str,
        purpose: str,
        has_consent: bool
    ) -> PolicyResponse:

        normalized_region = region.upper()
        normalized_age_group = age_group.lower()

        if normalized_age_group == "minor":
            return PolicyResponse(
                action=PolicyAction.DENY,
                reason="Advertising identity is not permitted for minors.",
                mode="blocked"
            )

        if normalized_region in {"EU", "EEA", "UK"}:
            if purpose == "advertising" and not has_consent:
                return PolicyResponse(
                    action=PolicyAction.DENY,
                    reason=(
                        "Advertising identity requires an affirmative "
                        "privacy choice under this prototype policy."
                    ),
                    mode="blocked"
                )

        if purpose == "advertising" and not has_consent:
            return PolicyResponse(
                action=PolicyAction.RESTRICT,
                reason=(
                    "Advertising identity is unavailable, but "
                    "contextual advertising may still be permitted."
                ),
                mode="contextual_only"
            )

        return PolicyResponse(
            action=PolicyAction.ALLOW,
            reason="Request satisfies the current prototype policy.",
            mode="pseudonymous_ads"
        )


policy_service = PolicyService()