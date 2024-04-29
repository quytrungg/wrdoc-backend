from rest_framework import mixins

from apps.core.api.views import BaseViewSet

from ...models import ConsultationTemplate
from .. import serializers


class ConsultationTemplateViewSet(
    mixins.ListModelMixin,
    BaseViewSet,
):
    """API viewset for viewing list of consultation templates."""

    queryset = ConsultationTemplate.objects.all()
    serializer_class = serializers.ConsultationTemplateSerializer
    search_fields = ()
    ordering_fields = ()
