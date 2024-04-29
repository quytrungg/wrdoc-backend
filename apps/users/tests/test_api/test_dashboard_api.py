from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User


def test_dashboard_api(api_client: APIClient, clinician_user: User) -> None:
    """Ensure authenticated user can view dashboard via API."""
    api_client.force_authenticate(clinician_user)
    response = api_client.get(reverse_lazy("v1:profile-get-dashboard"))
    assert response.status_code == status.HTTP_200_OK
