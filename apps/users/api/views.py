from django.db.models import Prefetch, QuerySet

from rest_framework import mixins, response
from rest_framework import serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from drf_spectacular.utils import extend_schema, inline_serializer
from localflavor.us import us_states

from libs.api.filter_backends import CustomDjangoFilterBackend
from libs.open_api.filters import OrderingFilterBackend

from apps.consultations.models import ConsultationRate
from apps.core.api.views import (
    BaseViewSet,
    ReadOnlyViewSet,
    StringOptionAPIView,
)
from apps.users.constants import SPECIALTY_TYPES, ClinicianType, PrivacyOptions
from apps.users.models import User

from ..services import get_dashboard_stats
from . import filters, serializers


class UsersViewSet(ReadOnlyViewSet):
    """ViewSet for viewing accounts."""

    queryset = User.objects.all().prefetch_related(
        Prefetch(
            "rates",
            queryset=ConsultationRate.objects.select_related("template"),
        ),
    )
    filterset_class = filters.UserFilter
    serializer_class = serializers.UserListSerializer
    serializers_map = {
        "retrieve": serializers.UserDetailSerializer,
        "default": serializers.UserDetailSerializer,
    }
    filter_backends = (CustomDjangoFilterBackend, OrderingFilterBackend)
    ordering_fields = ()

    # pylint: disable=no-member
    def get_queryset(self):
        """If no params are provided, filter with current user's specialty."""
        qs = super().get_queryset()
        query_param_list = self.request.query_params
        filter_list = self.filterset_class.declared_filters.keys()
        is_filter_provided = bool(
            query_param_list and any(
                param in filter_list and value
                for param, value in query_param_list.items()
            ),
        )
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = self.request.user
        if self.action == "list" and not is_filter_provided:
            qs = qs.filter(
                specialty__overlap=user.specialty,
                clinician_type=user.clinician_type,
                primary_region_practice_state=(
                    user.primary_region_practice_state
                ),
            ).exclude(id=user.id)
        return qs.with_has_contact(user).with_total_contacts()


# pylint: disable=unused-argument
class UserProfileViewSet(
    BaseViewSet,
):
    """APIs for retrieving user profile."""

    queryset = QuerySet()
    serializer_class = serializers.UserDetailSerializer

    def get_object(self) -> User:
        """Return the current logged-in user."""
        return self.request.user

    @extend_schema(
        responses={"200": serializers.ResponsePrivacySettingsSerializer},
    )
    @action(
        detail=False,
        methods=("get", "put"),
        serializer_class=serializers.PrivacySettingsSerializer,
    )
    def privacy_settings(self, request, *args, **kwargs) -> response.Response:
        """Handle requests to privacy settings."""
        if request.method in ("put", "PUT"):
            return self._update_privacy_settings(request)
        return self._get_privacy_settings(request)

    @action(
        detail=False,
        methods=("get",),
        serializer_class=serializers.DashboardSerializer,
        url_path="dashboard",
    )
    def get_dashboard(self, request, *args, **kwargs) -> response.Response:
        """Return dashboard data for current user."""
        user = self.get_object()
        dashboard_stats = get_dashboard_stats(user)
        serializer = self.get_serializer(dashboard_stats)
        return response.Response(serializer.data)

    @extend_schema(
        request=None,
        responses={
            "200": inline_serializer(
                name="ConnectedAccountLink",
                fields={
                    "url": drf_serializers.CharField(),
                },
            ),
        },
    )
    @action(
        detail=False,
        methods=("post",),
        url_path="create-connected-account",
    )
    def create_connected_account(
        self,
        request,
        *args,
        **kwargs,
    ) -> response.Response:
        """Create connected account for current user."""
        user = self.get_object()
        account_link = user.get_account_link()
        return response.Response(
            data={
                "url": account_link.url,
            },
        )

    @extend_schema(
        responses={
            "200": inline_serializer(
                name="ConnectedAccountParameters",
                fields={
                    "details_submitted": drf_serializers.CharField(),
                    "charges_enabled": drf_serializers.CharField(),
                },
            ),
        },
    )
    @action(
        detail=False,
        methods=("get",),
        url_path="get-connected-account",
    )
    def get_connected_account(
        self,
        request,
        *args,
        **kwargs,
    ) -> response.Response:
        """Fetch onboard info for related Stripe Account."""
        user = self.get_object()
        account = user.get_stripe_account()
        return response.Response(
            data={
                "details_submitted": account["details_submitted"],
                "charges_enabled": account["charges_enabled"],
            },
        )

    def _update_privacy_settings(self, request) -> response.Response:
        """Update privacy settings for current user."""
        user = self.get_object()
        serializer = serializers.PrivacySettingsSerializer(
            instance=user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    # pylint: disable=unused-argument
    def _get_privacy_settings(self, request) -> response.Response:
        """Return privacy settings for current user."""
        user = self.get_object()
        serializer = serializers.PrivacySettingsSerializer(
            user.privacy_settings,
        )
        return response.Response(serializer.data)


class UserProfileRetrieveUpdateViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    UserProfileViewSet,
):
    """Custom url mapping for update and retrieve user profile."""

    ordering_fields = ()
    search_fields = ()

    def list(self, request, *args, **kwargs):
        """Handle get profile request."""
        return self.retrieve(request, *args, **kwargs)


class ContactViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Viewset to return user's contact information."""

    queryset = User.objects.all()
    filterset_class = filters.UserContactFilter
    serializer_class = serializers.UserDetailSerializer
    serializers_map = {
        "create": serializers.ContactSerializer,
        "default": serializers.UserDetailSerializer,
    }
    filter_backends = (CustomDjangoFilterBackend, OrderingFilterBackend)
    ordering_fields = ()

    def get_queryset(self):
        """Filter users by contact."""
        qs = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = self.request.user
        return qs.filter(
            id__in=user.contacts.values("contact"),
        ).with_has_contact(user).with_total_contacts()

    def get_object(self):
        """Return contact object on delete."""
        if self.action == "destroy":
            user = self.request.user
            return get_object_or_404(
                user.contacts.all(),
                contact=self.kwargs["pk"],
            )
        return super().get_object()


class StateChoiceAPIView(StringOptionAPIView):
    """List available US's state choices."""

    option_list = us_states.US_STATES


class ClinicianChoiceAPIView(StringOptionAPIView):
    """List available clinician types."""

    option_list = ClinicianType.choices


class SpecialtyChoiceAPIView(StringOptionAPIView):
    """List available specialty types."""

    option_list = SPECIALTY_TYPES


class PrivacyChoiceAPIView(StringOptionAPIView):
    """List available privacy options."""

    option_list = PrivacyOptions.choices
