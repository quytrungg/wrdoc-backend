from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

from apps.consultations.models import ConsultationTemplate
from apps.users.models import User

consultation_template_list_api = reverse_lazy("v1:consultation-template-list")


def test_consultation_template_list_api(
    api_client: APIClient,
    student_user: User,
    templates: list[ConsultationTemplate],
) -> None:
    """Ensure users can view requested from/by consultations."""
    api_client.force_authenticate(student_user)
    response = api_client.get(consultation_template_list_api)
    assert response.status_code == status.HTTP_200_OK, response.data
