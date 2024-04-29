from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class StripeCustomer(BaseModel):
    """Store stripe Customer information."""

    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="stripe_customers",
    )
    stripe_id = models.CharField(
        verbose_name=_("Stripe ID"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Stripe Customer")
        verbose_name_plural = _("Stripe Customers")

    def __str__(self):
        return f"Stripe Customer for User {self.user_id}"
