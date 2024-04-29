from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

from ..services.stripe.customer import create_customer
from ..services.stripe.payment_method import attach_payment_method
from ..services.stripe.session import (
    retrieve_checkout_session,
    retrieve_setup_intent,
)


class AttachPaymentMethodSerializer(OpenApiSerializer):
    """Represent serializer to attach payment method to customer."""

    session_id = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        fields = (
            "session_id",
        )

    def validate_session_id(self, session_id: str) -> str:
        """Verify session id and get payment method id from setup intent."""
        try:
            session = retrieve_checkout_session(session_id)
            setup_intent_id = session["data"]["setup_intent"]
            setup_intent = retrieve_setup_intent(setup_intent_id)
            payment_method_id = setup_intent["payment_method"]
            return payment_method_id
        except Exception as err:
            raise serializers.ValidationError(
                _("Invalid session id. Please check again."),
            ) from err

    def save(self, **kwargs) -> None:
        """Retrieve payment method from setup intent and attach to customer."""
        payment_method_id = self.validated_data["session_id"]
        user = self.context["request"].user
        customer = create_customer(user)
        attach_payment_method(
            customer_id=customer.id,
            payment_method_id=payment_method_id,
        )
