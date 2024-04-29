from dataclasses import asdict, dataclass, field

from .constants import PHONE_NUMBER_LENGTH, PrivacyFields, PrivacyOptions


def is_valid_phone_number(phone_number: str) -> bool:
    """Validate `phone_number` is a string of 10 numbers."""
    return len(phone_number) == PHONE_NUMBER_LENGTH and phone_number.isdigit()


def is_valid_npi_number(npi_number: str) -> bool:
    """Validate `npi_number`, currently have the same logic as phone."""
    return is_valid_phone_number(npi_number)


@dataclass
class PrivacySetting:
    """Privacy settings."""

    type: str
    users: list[int] = field(default_factory=list)


def default_privacy_settings() -> dict[str, dict]:
    """Generate default privacy settings for user."""
    return {
        privacy_field: asdict(PrivacySetting(PrivacyOptions.PUBLIC))
        for privacy_field in PrivacyFields
    }
