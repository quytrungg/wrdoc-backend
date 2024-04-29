from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...models import ConsultationRate
from .. import serializers


class ConsultationRateAPIView(GenericAPIView):
    """API viewset for viewing user's consultation rates."""

    queryset = ConsultationRate.objects.all().select_related("template")
    serializer_class = serializers.ConsultationRateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "user_id"

    def get(self, *args, **kwargs) -> Response:
        """Return list of consultation rates from user id."""
        user_id = kwargs.get("user_id")
        consultation_rate = super().get_queryset().filter(user_id=user_id)
        serializer = self.serializer_class(consultation_rate, many=True)
        return Response(data={"results": serializer.data})
