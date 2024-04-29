from django.db import models
from django.utils.translation import gettext_lazy as _

import stripe.checkout

from apps.core.models import BaseModel
from apps.payments.services.stripe.session import retrieve_checkout_session


class StripeCheckoutSession(BaseModel):
    """Store Stripe Checkout Session information."""

    stripe_id = models.CharField(
        _("Stripe ID"),
        max_length=255,
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
    )
    consultation = models.ForeignKey(
        to="consultations.Consultation",
        on_delete=models.CASCADE,
        verbose_name=_("Consultation"),
        related_name="checkout_session",
    )

    class Meta:
        verbose_name = _("Stripe Checkout Session")
        verbose_name_plural = _("Stripe Checkout Sessions")

    def __str__(self):
        return (
            f"Stripe Checkout session for "
            f"consultation {self.consultation_id}"
        )

    def get_stripe_data(self) -> stripe.checkout.Session:
        """Return Stripe object of Checkout Session."""
        return retrieve_checkout_session(self.stripe_id)
