from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from . import models, notifications


def reset_user_password(
    user: models.User,
) -> bool:
    """Reset user password.

    This will send to user an email with a link where user can enter new
    password.

    """
    return notifications.UserPasswordResetEmailNotification(
        user=user,
        uid=urlsafe_base64_encode(force_bytes(user.pk)),
        token=PasswordResetTokenGenerator().make_token(user),
    ).send()


def get_dashboard_stats(user: models.User) -> dict:
    """Return dashboard stats for user."""
    received_consultation_cost = user.received_consultations.all().values_list(
        "cost",
        flat=True,
    )
    stats = {
        "consultation_count": len(received_consultation_cost),
        "request_count": user.created_consultations.count(),
        "earnings": sum(received_consultation_cost),
    }
    return stats
