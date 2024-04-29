from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from apps.users.models import User

video_auth_url = reverse_lazy("v1:video-auth")


@pytest.fixture
def video_auth_data() -> dict:
    """Return video auth data."""
    return {
        "role_type": "1",
        "tpc": "sample_session_name",
        "user_identity": "sample_user_identity",
        "session_key": "sample_session_key",
    }


def test_video_auth_create_api(
    api_client: APIClient,
    clinician_user: User,
    video_auth_data: dict,
) -> None:
    """Ensure authenticated users can get jwt token from video auth api."""
    api_client.force_authenticate(clinician_user)
    response = api_client.post(video_auth_url, video_auth_data)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data.get("signature")


def test_video_auth_create_api_without_session_key(
    api_client: APIClient,
    clinician_user: User,
    video_auth_data: dict,
) -> None:
    """Ensure users with role host/co-host must provide session key."""
    api_client.force_authenticate(clinician_user)
    video_auth_data.pop("session_key")
    response = api_client.post(video_auth_url, video_auth_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
