from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class StripeAccount(BaseModel):
    """Store stripe Account information."""

    user = models.OneToOneField(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="stripe_account",
    )
    stripe_id = models.CharField(
        verbose_name=_("Stripe ID"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Stripe Account")
        verbose_name_plural = _("Stripe Accounts")

    def __str__(self):
        return f"Stripe Account for User {self.user_id}"
