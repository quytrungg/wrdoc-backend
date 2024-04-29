from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from apps.core.test_utils import get_test_file_url
from apps.users.constants import ClinicianType, PrivacyFields, PrivacyOptions
from apps.users.models import User

user_profile_api = reverse_lazy("v1:profile")
user_privacy_settings_api = reverse_lazy("v1:profile-privacy-settings")


@pytest.fixture
def profile_update_data(create_file) -> dict:
    """Return user profile updated data."""
    return {
        "first_name": "First",
        "last_name": "Last",
        "username": "username",
        "entity": "Updated Entity",
        "pronoun": "he/him",
        "clinician_type": ClinicianType.MD,
        "graduation_date": "2024-03-11",
        "email": "user@example.com",
        "secondary_email": "user2@example.com",
        "phone_number": "1234567890",
        "address": "1234567890",
        "primary_region_practice_state": "CA",
        "primary_region_practice_zip": "70000",
        "address_state": "CA",
        "address_zip": "70000",
        "fax_number": "1234567890",
        "avatar": get_test_file_url(create_file("avatar.jpg")),
        "description": "About Me",
        "specialty": ["Updated Specialty 1", "Updated Specialty 2"],
        "specialty_area": "Updated Specialty Area",
    }


def test_user_profile_retrieve_api(
    clinician_user: User,
    api_client: APIClient,
) -> None:
    """Ensure authenticated user can view profile via API."""
    api_client.force_authenticate(clinician_user)
    response = api_client.get(user_profile_api)
    assert response.status_code == status.HTTP_200_OK


def test_user_profile_update_api(
    student_user: User,
    api_client: APIClient,
    profile_update_data: dict,
) -> None:
    """Ensure authenticated user can update profile via API."""
    api_client.force_authenticate(student_user)
    response = api_client.put(user_profile_api, data=profile_update_data)
    assert response.status_code == status.HTTP_200_OK, response.data


def test_user_profile_privacy_settings_get_api(
    api_client,
    clinician_user,
):
    """Ensure privacy settings could be fetched."""
    api_client.force_authenticate(clinician_user)
    response = api_client.get(user_privacy_settings_api)
    assert response.status_code == status.HTTP_200_OK


def test_user_profile_privacy_settings_update_api(
    api_client,
    clinician_user,
    student_user,
):
    """Ensure privacy settings can be updated."""
    api_client.force_authenticate(clinician_user)
    privacy_settings = clinician_user.privacy_settings
    privacy_settings[PrivacyFields.ABOUT_ME.value] = {
        "type": PrivacyOptions.CUSTOM,
        "users": [student_user.id],
    }
    response = api_client.put(user_privacy_settings_api, data=privacy_settings)
    assert response.status_code == status.HTTP_200_OK
