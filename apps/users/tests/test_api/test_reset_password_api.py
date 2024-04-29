import re
import typing

from django.conf import settings
from django.core import mail
from django.urls import reverse_lazy

from rest_framework import status, test
from rest_framework.response import Response

from ... import factories, models, notifications, services


def _get_reset_token_from_email(user_email: str) -> typing.Tuple[str, str]:
    """Extract reset token from email."""
    subject = (
        f"{settings.APP_LABEL} - "
        f"{notifications.UserPasswordResetEmailNotification.subject}"
    )
    reset_email = next(
        email for email in mail.outbox
        if email.subject == subject and email.to == [user_email]
    )
    token_matches = re.findall(
        pattern=r"(?=token=(.*)\")",
        string=reset_email.alternatives[0][0],
    )
    uid, *token_parts = token_matches[0].split("-")
    return uid, "-".join(token_parts)


def test_password_reset(user_api_client: test.APIClient, user: models.User):
    """Test that user can request password rest and it will sent it email."""
    for info in (user.email, user.username, user.npi_number):
        response: Response = user_api_client.post(
            path=reverse_lazy("v1:password-reset"),
            data={"information": info},
        )
        assert response.status_code == status.HTTP_200_OK, response.data
        # Check that email was sent and contains needed token
        assert _get_reset_token_from_email(user_email=user.email)


def test_password_reset_confirm(
    user_api_client: test.APIClient,
    user: models.User,
):
    """Test that user can change password with token."""
    services.reset_user_password(user=user)
    uid, token = _get_reset_token_from_email(user_email=user.email)
    new_password = factories.DEFAULT_PASSWORD + "?"
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    # Check that password was indeed changed
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:login"),
        data={
            "username": user.email,
            "password": factories.DEFAULT_PASSWORD,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:login"),
        data={
            "username": user.email,
            "password": new_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data


def test_password_reset_confirm_reuse(
    user_api_client: test.APIClient,
    user: models.User,
):
    """Test that user can't reuse token for password change."""
    services.reset_user_password(user=user)
    uid, token = _get_reset_token_from_email(user_email=user.email)
    new_password = factories.DEFAULT_PASSWORD + "?"
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert (
        response.data["errors"][0]["detail"] == "Invalid token"
    ), response.data


def test_password_reset_confirm_token_validation(
    user_api_client: test.APIClient,
    user: models.User,
):
    """Test validation against invalid uid."""
    response: Response = user_api_client.post(
        path=reverse_lazy("v1:password-reset-confirm"),
        data={
            "password": "password",
            "password_confirm": "password",
            "uid": "uid",
            "token": "token",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert response.data["errors"][0]["detail"] == "Invalid uid", response.data
