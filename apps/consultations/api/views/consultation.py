from django.db.models import Q

from rest_framework import mixins, response
from rest_framework import serializers as drf_serializers
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, inline_serializer

from apps.core.api import mixins as core_mixins
from apps.core.api.views import BaseViewSet, StringOptionAPIView

from ... import models
from ...constants import SessionType
from .. import permissions, serializers
from ..filters import ConsultationFilter


# pylint: disable=unused-argument,duplicate-code
class ConsultationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    core_mixins.UpdateModelWithoutPatchMixin,
    BaseViewSet,
):
    """API viewset to manage consultations."""

    queryset = models.Consultation.objects.all()
    filterset_class = ConsultationFilter
    serializer_class = serializers.ConsultationReadSerializer
    serializers_map = {
        "create": serializers.ConsultationCreateSerializer,
        "update": serializers.ConsultationUpdateSerializer,
        "default": serializers.ConsultationReadSerializer,
    }
    permissions_map = {
        "update": (
            permissions.CanAcceptConsultation,
            permissions.CanDeclineConsultation,
            permissions.CanCancelConsultation,
        ),
        "checkout": (permissions.IsReceivedConsultation,),
    }
    search_fields = ()
    ordering_fields = (
        "created",
    )

    def get_queryset(self):
        """Return consultations that are requested from/to request user."""
        qs = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = self.request.user
        return qs.filter(Q(from_user=user) | Q(to_user=user))

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="ConsultationCheckout",
                fields={
                    "client_secret": drf_serializers.CharField(),
                },
            ),
        },
    )
    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        """Start checkout session for consultation."""
        consultation = self.get_object()
        session = consultation.get_checkout_session()
        return response.Response(
            data={
                "client_secret": session.client_secret,
            },
        )


class SessionTypeChoiceAPIView(StringOptionAPIView):
    """List available session types."""

    option_list = SessionType.choices
