from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from apps.users.constants import ClinicianType, UserRole
from apps.users.factories import DEFAULT_PASSWORD, UserFactory
from apps.users.models import User

user_register_api = reverse_lazy("v1:register")


@pytest.fixture
def user_registration_data() -> dict:
    """User registration data."""
    return {
        "email": "user@example.com",
        "password": DEFAULT_PASSWORD,
        "password_confirm": DEFAULT_PASSWORD,
        "first_name": "first",
        "last_name": "last",
        "entity": "Test entity",
        "username": "testuser",
        "pronoun": "he/him",
        "clinician_type": str(ClinicianType.PA.value),
        "specialty": "Test specialty",
        "role": str(UserRole.CLINICIAN.value),
        "npi_number": "1234567890",
        "graduation_date": "2024-03-01",
        "primary_region_practice_state": "CA",
        "primary_region_practice_zip": "70000",
        "address_state": "CA",
        "address_zip": "70000",
        "secondary_email": "user2@example.com",
        "allow_notifications": True,
        "phone_number": "1234567890",
        "address": "Test address",
        "fax_number": "1234567890",
        "signature": "first last",
    }


@pytest.fixture
def registration_data_invalid_username(
    user_registration_data: dict,
    clinician_user: User,
) -> dict:
    """Return registration data with existing username."""
    user_registration_data["username"] = clinician_user.username
    return user_registration_data


@pytest.fixture
def registration_data_mismatch_password(user_registration_data: dict) -> dict:
    """Return registration data with mismatched password."""
    user_registration_data["password_confirm"] = ""
    return user_registration_data


@pytest.fixture
def clinician_registration_data_without_npi(
    user_registration_data: dict,
) -> dict:
    """Return registration data without NPI number."""
    user_registration_data["role"] = str(UserRole.CLINICIAN.value)
    user_registration_data.pop("npi_number")
    return user_registration_data


@pytest.fixture
def registration_data_invalid_secondary_email(
    user_registration_data: dict,
    student_user: User,
) -> dict:
    """Return registration data with invalid secondary email."""
    user_registration_data["secondary_email"] = student_user.email
    return user_registration_data


def test_user_register_api(
    api_client: APIClient,
    user_registration_data: dict,
) -> None:
    """Ensure everyone can register a new account via API."""
    if user := User.objects.filter(
        npi_number=user_registration_data["npi_number"],
    ).first():
        user.delete()
    response = api_client.post(user_register_api, data=user_registration_data)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data["token"]


@pytest.mark.parametrize(
    ["invalid_registration_data", "expected_status_code"],
    [
        [
            pytest.lazy_fixture("registration_data_invalid_username"),
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            pytest.lazy_fixture("registration_data_mismatch_password"),
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            pytest.lazy_fixture("clinician_registration_data_without_npi"),
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            pytest.lazy_fixture("registration_data_invalid_secondary_email"),
            status.HTTP_400_BAD_REQUEST,
        ],
    ],
)
def test_user_register_api_invalid_data(
    api_client: APIClient,
    invalid_registration_data: dict,
    expected_status_code: int,
) -> None:
    """Ensure invalid data can't be used to register a new account."""
    response = api_client.post(
        user_register_api,
        data=invalid_registration_data,
    )
    assert response.status_code == expected_status_code, response.data


def test_user_register_api_with_existing_npi_number(
    api_client: APIClient,
    user_registration_data: dict,
) -> None:
    """Ensure user can register with existing NPI number."""
    UserFactory(npi_number=user_registration_data["npi_number"])
    response = api_client.post(user_register_api, data=user_registration_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
