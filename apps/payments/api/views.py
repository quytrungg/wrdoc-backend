from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from libs.open_api.serializers import OpenApiSerializer

from apps.payments.services.stripe.session import create_checkout_session

from . import serializers


# pylint: disable=unused-argument
class CheckoutSessionAPIView(GenericAPIView):
    """Represent API view for create and get stripe checkout session."""

    serializer_class = OpenApiSerializer
    queryset = QuerySet()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        """Create stripe checkout session."""
        return Response(data={"data": create_checkout_session()})


class AttachPaymentMethodAPIView(GenericAPIView):
    """Represent API view to create customer and attach payment method."""

    serializer_class = serializers.AttachPaymentMethodSerializer
    queryset = QuerySet()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        """Create stripe customer and attach payment method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"data": _("Attach payment method successfully.")},
        )
