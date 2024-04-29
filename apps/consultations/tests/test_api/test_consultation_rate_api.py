from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User


def test_consultation_rate_list_api(
    api_client: APIClient,
    student_user: User,
) -> None:
    """Ensure users can view requested from/by consultations."""
    api_client.force_authenticate(student_user)
    url = reverse_lazy(
        "v1:consultation-rate",
        kwargs={"user_id": student_user.id},
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data["results"]) == student_user.rates.count()
