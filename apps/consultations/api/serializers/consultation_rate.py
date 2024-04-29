from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.core.api.serializers import (
    DecimalField,
    ModelBaseSerializer,
    NestedCreateUpdateListSerializer,
)

from ...models import ConsultationRate


class ConsultationRateNestedSerializer(NestedCreateUpdateListSerializer):
    """Provide custom uneditable fields for consultation rates."""

    uneditable_fields = ("id", "pk", "template")

    def validate(self, attrs) -> dict:
        """Ensure only `id` or `templated` is provided for create/udpate."""
        attrs = super().validate(attrs)
        template_ids = [rate.get("template") for rate in attrs]
        if all(template_ids) and len(set(template_ids)) != len(template_ids):
            raise serializers.ValidationError(
                _("Can't create rates with duplicate templates."),
            )
        return attrs

    def get_data_for_insertion(self, instances_mapping, validated_data):
        """Disable create operation for consultation rates when update."""
        return []

    def get_instances_for_deletion(self, instances_mapping, validated_data):
        """Disable delete operation for consultation rates when update."""
        return {}


class ConsultationRateSerializer(ModelBaseSerializer):
    """Represent serializer for ConsultationRate model."""

    id = serializers.IntegerField(
        required=False,
        help_text=_("Provide this field for updating user's rate."),
    )
    session_type = serializers.CharField(
        source="template.session_type",
        read_only=True,
    )
    duration = serializers.IntegerField(
        source="template.duration",
        read_only=True,
    )
    rate = DecimalField(allow_null=True)
    fee = DecimalField(source="template.fee", read_only=True)

    class Meta:
        model = ConsultationRate
        list_serializer_class = ConsultationRateNestedSerializer
        fields = (
            "id",
            "template",
            "session_type",
            "duration",
            "rate",
            "fee",
            "allow_offered",
        )
        extra_kwargs = {
            "template": {
                "required": False,
                "help_text": _("Provide this field for creating user's rate."),
            },
        }

    def validate(self, attrs) -> dict:
        """Ensure only `id` or `templated` is provided for create/udpate."""
        attrs = super().validate(attrs)
        if attrs.get("id") and attrs.get("template"):
            raise serializers.ValidationError(
                _("Can't create and update rate at the same time."),
            )
        return attrs
