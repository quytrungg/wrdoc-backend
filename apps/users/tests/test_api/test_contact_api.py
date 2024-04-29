from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from apps.users.constants import UserRole
from apps.users.factories import ContactFactory, UserFactory
from apps.users.models import Contact, User


def test_user_contacts_list_api(
    clinician_user: User,
    api_client: APIClient,
) -> None:
    """Ensure contact list is returned."""
    ContactFactory(owner=clinician_user)
    ContactFactory()
    api_client.force_authenticate(clinician_user)
    response = api_client.get(reverse_lazy("v1:contact-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


def test_user_contact_create_api(
    clinician_user: User,
    api_client: APIClient,
) -> None:
    """Ensure contact could be created by user id."""
    contact_user = UserFactory(role=UserRole.CLINICIAN)
    api_client.force_authenticate(clinician_user)
    response = api_client.post(
        reverse_lazy("v1:contact-list"),
        data={"contact": contact_user.id},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Contact.objects.filter(
        owner=clinician_user,
        contact=contact_user,
    ).exists()


def test_user_contact_delete_api(
    clinician_user: User,
    api_client: APIClient,
) -> None:
    """Ensure contact could be removed by user id."""
    contact = ContactFactory(owner=clinician_user)
    api_client.force_authenticate(clinician_user)
    response = api_client.delete(
        reverse_lazy("v1:contact-detail", kwargs={"pk": contact.contact_id}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Contact.objects.filter(
        owner=clinician_user,
        contact=contact.contact,
    ).exists()
