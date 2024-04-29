from functools import partial

from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from apps.users.constants import ClinicianType
from apps.users.factories import UserFactory
from apps.users.models import User


def get_user_url(action_name: str, kwargs=None):
    """Return url for user's APIs."""
    return reverse_lazy(f"v1:user-{action_name}", kwargs=kwargs)


user_list_api = partial(get_user_url, action_name="list")()
user_detail_api = partial(get_user_url, action_name="detail")


@pytest.fixture
def user_list() -> list[User]:
    """Return list of users."""
    return (
        UserFactory.create_batch(
            size=3,
            clinician_type=ClinicianType.PA,
            specialty=["Neuroscience"],
        )
        + UserFactory.create_batch(
            size=2,
            clinician_type=ClinicianType.PA_AA,
            specialty=["Neurosurgery"],
        )
    )


def test_user_list_api(api_client: APIClient, user_list: list[User]) -> None:
    """Ensure authenticated user can view and filter user list via API."""
    # create user with different clinician type compared to search term
    user = UserFactory(clinician_type=ClinicianType.STU)
    api_client.force_authenticate(user)
    response = api_client.get(user_list_api, data={"search": "physician"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] >= User.objects.filter(
        clinician_type__icontains="pa",
    ).count()


def test_user_detail_api(api_client: APIClient, clinician_user: User) -> None:
    """Ensure authenticated user can view user detail via API."""
    api_client.force_authenticate(clinician_user)
    response = api_client.get(
        user_detail_api(kwargs={"pk": clinician_user.id}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == clinician_user.id
