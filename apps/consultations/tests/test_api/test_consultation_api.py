from functools import partial

from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from apps.consultations.constants import (
    CONSULTATION_FEE_RATE,
    ConsultationStatus,
    SessionType,
)
from apps.consultations.factories import ConsultationAttachmentFactory
from apps.consultations.models import Consultation
from apps.core.test_utils import get_test_file_url
from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture
def consultation_create_data(clinician_user: User, create_file) -> dict:
    """Return consultation data for create API."""
    return {
        "to_user": clinician_user.id,
        "session_type": str(SessionType.CONSULTATION.value),
        "attachments": [
            {"file": get_test_file_url(create_file("test1.png"))},
            {"file": get_test_file_url(create_file("test2.png"))},
        ],
        "description": "This is a test consultation.",
        "note": "This is a test note.",
        "duration": 20,
        "cost": 100,
        "fee": CONSULTATION_FEE_RATE,
    }


@pytest.fixture
def consultation_update_data(create_file) -> dict:
    """Return consultation data for update API."""
    return {
        "attachments": [
            {"file": get_test_file_url(create_file("test3.png"))},
            {"file": get_test_file_url(create_file("test4.png"))},
            {"file": get_test_file_url(create_file("test5.png"))},
        ],
        "description": "Updated consultation.",
        "note": "Updated note.",
        "duration": 40,
        "cost": 200,
        "fee": CONSULTATION_FEE_RATE,
    }


def get_consultation_url(action_name: str, kwargs=None):
    """Return url for consultation's APIs."""
    return reverse_lazy(f"v1:consultation-{action_name}", kwargs=kwargs)


consultation_list_api = partial(get_consultation_url, action_name="list")()
consultation_detail_api = partial(get_consultation_url, action_name="detail")


def test_consultation_list_api(
    api_client: APIClient,
    consultations: list[Consultation],
) -> None:
    """Ensure users can view requested from/by consultations."""
    user = consultations[0].from_user
    api_client.force_authenticate(user)
    response = api_client.get(consultation_list_api)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data["count"] == Consultation.objects.filter(
        from_user=user,
    ).count()


def test_consultation_detail_api(
    api_client: APIClient,
    consultation: Consultation,
) -> None:
    """Ensure users can view consultation detail."""
    api_client.force_authenticate(consultation.from_user)
    response = api_client.get(
        consultation_detail_api(kwargs={"pk": consultation.id}),
    )
    assert response.status_code == status.HTTP_200_OK, response.data


def test_consultation_create_api(
    api_client: APIClient,
    student_user: User,
    consultation_create_data: dict,
) -> None:
    """Ensure users can create consultation with valid data."""
    api_client.force_authenticate(student_user)
    response = api_client.post(
        consultation_list_api,
        data=consultation_create_data,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert response.data["to_user"] == consultation_create_data["to_user"]
    assert response.data["status"] == ConsultationStatus.REQUESTED
    assert len(response.data["attachments"]) == len(
        consultation_create_data["attachments"],
    )


def test_consultation_create_api_invalid_user(
    api_client: APIClient,
    student_user: User,
    consultation_create_data: dict,
) -> None:
    """Ensure users can't create consultation to themselves."""
    api_client.force_authenticate(student_user)
    invalid_data = {
        **consultation_create_data,
        "to_user": student_user.id,
    }
    response = api_client.post(consultation_list_api, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_consultation_create_api_rate_not_found(
    api_client: APIClient,
    student_user: User,
    consultation_create_data: dict,
) -> None:
    """Ensure consultation with not found duration will get errors."""
    # duration not found for 10 minutes
    consultation_create_data["duration"] = 10
    api_client.force_authenticate(student_user)
    response = api_client.post(
        consultation_list_api,
        data=consultation_create_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_consultation_create_api_rate_not_allow_offered(
    api_client: APIClient,
    student_user: User,
    consultation_create_data: dict,
) -> None:
    """Ensure users can't offer price to user with rate and not allow offer."""
    requested_user = UserFactory()
    chosen_rate = requested_user.rates.first()
    chosen_template = chosen_rate.template
    chosen_rate.allow_offered = False
    chosen_rate.rate = 30
    chosen_rate.save()
    consultation_create_data.update(
        {
            "to_user": requested_user.id,
            "session_type": chosen_template.session_type,
            "duration": chosen_template.duration,
        },
    )
    api_client.force_authenticate(student_user)
    response = api_client.post(
        consultation_list_api,
        data=consultation_create_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_consultation_update_api(
    api_client: APIClient,
    consultation: Consultation,
    consultation_update_data: dict,
) -> None:
    """Ensure users can update allowed data when consultation is requested."""
    api_client.force_authenticate(consultation.from_user)
    response = api_client.put(
        consultation_detail_api(kwargs={"pk": consultation.id}),
        data=consultation_update_data,
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    consultation.refresh_from_db()
    assert consultation.attachments.count() == len(
        consultation_update_data["attachments"],
    )


def test_consultation_update_api_without_attachments(
    api_client: APIClient,
    consultation: Consultation,
    consultation_update_data: dict,
) -> None:
    """Ensure users can update consultation without any attachment changes."""
    ConsultationAttachmentFactory.create_batch(2, consultation=consultation)
    consultation_update_data["attachments"] = None
    api_client.force_authenticate(consultation.from_user)
    response = api_client.put(
        consultation_detail_api(kwargs={"pk": consultation.id}),
        data=consultation_update_data,
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    consultation.refresh_from_db()
    assert consultation.attachments.count() == 2


def test_consultation_update_api_after_accepted(
    api_client: APIClient,
    consultation: Consultation,
    consultation_update_data: dict,
) -> None:
    """Ensure users can only update note after consultation is accepted."""
    api_client.force_authenticate(consultation.from_user)
    consultation.accept()
    response = api_client.put(
        consultation_detail_api(kwargs={"pk": consultation.id}),
        data=consultation_update_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data["errors"]) == len(
        ["duration", "cost", "description", "attachments"],
    )
