from rest_framework import mixins, response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from . import mixins as core_mixins
from .serializers import StringOptionSerializer


class BaseViewSet(
    core_mixins.ActionPermissionsMixin,
    core_mixins.ActionSerializerMixin,
    GenericViewSet,
):
    """Base viewset for api."""

    base_permission_classes = (IsAuthenticated,)

    def get_viewset_permissions(self):
        """Prepare viewset permissions.

        Method returns union of `base_permission_classes` and
        `permission_classes`, specified in child classes.

        """
        extra_permissions = tuple(
            permission for permission in self.permission_classes
            if permission not in self.base_permission_classes
        )
        permissions = self.base_permission_classes + extra_permissions
        return [permission() for permission in permissions]


class CRUDViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    core_mixins.UpdateModelWithoutPatchMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """CRUD viewset for api views."""


class ReadOnlyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    BaseViewSet,
):
    """Read only viewset for api views."""


class StringOptionAPIView(GenericAPIView):
    """List all available string options, allow all requests."""

    serializer_class = StringOptionSerializer
    permission_classes = (AllowAny,)
    option_list = ()

    def get(self, *args, **kwargs) -> response.Response:
        """Return all available string options."""
        data = [
            {"value": abbr, "label": name} for abbr, name in self.option_list
        ]
        serializer = self.get_serializer(data, many=True)
        return response.Response(data={"results": serializer.data})
