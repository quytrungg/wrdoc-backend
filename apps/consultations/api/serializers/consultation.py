from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.core.api.serializers import ModelBaseSerializer
from apps.core.exceptions import NonFieldValidationError
from apps.users.api.serializers import UserDetailSerializer
from apps.users.models import User

from ... import exceptions, models
from ...constants import (
    CONSULTATION_STATUS_ACTION_MAP,
    ConsultationStatus,
    SessionType,
)
from ..mixins import ConsultationTotalCostMixin
from .consultation_attachment import ConsultationAttachmentSerializer


class ConsultationReadSerializer(
    ConsultationTotalCostMixin,
    ModelBaseSerializer,
):
    """Represent serializer for list/retrieve APIs in Consultation model."""

    from_user = UserDetailSerializer()
    to_user = UserDetailSerializer()
    total_cost = serializers.SerializerMethodField()
    attachments = ConsultationAttachmentSerializer(many=True)

    class Meta:
        model = models.Consultation
        fields = (
            "id",
            "from_user",
            "to_user",
            "status",
            "created",
            "session_type",
            "attachments",
            "description",
            "note",
            "duration",
            "cost",
            "fee",
            "total_cost",
            "completed_at",
        )


class ConsultationCreateSerializer(
    ConsultationTotalCostMixin,
    ModelBaseSerializer,
):
    """Represent serializer for create API in Consultation model."""

    from_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    session_type = serializers.ChoiceField(choices=SessionType.choices)
    total_cost = serializers.SerializerMethodField()
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",
        read_only=True,
    )
    attachments = ConsultationAttachmentSerializer(
        many=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = models.Consultation
        fields = (
            "id",
            "from_user",
            "to_user",
            "status",
            "created",
            "session_type",
            "attachments",
            "description",
            "note",
            "duration",
            "cost",
            "fee",
            "total_cost",
            "completed_at",
        )
        read_only_fields = (
            "status",
            "completed_at",
        )

    def validate(self, attrs: dict) -> dict:
        """Ensure cost is suitable with user's rate/offered price."""
        attrs = super().validate(attrs)
        chosen_rate = models.ConsultationRate.objects.filter(
            user=attrs["to_user"],
            template__session_type=attrs["session_type"],
            template__duration=attrs["duration"],
        ).first()
        if not chosen_rate:
            raise serializers.ValidationError(
                _("Consultation rate not found."),
            )
        if not chosen_rate.allow_offered and attrs["cost"] != chosen_rate.rate:
            raise serializers.ValidationError(
                _("Can't offer price for this consultation."),
            )
        return attrs

    def create(self, validated_data: dict) -> models.Consultation:
        """Add attachments to consultation."""
        attachments_data = validated_data.pop("attachments", [])
        consultation = super().create(validated_data)
        for attachment_data in attachments_data:
            attachment_data["consultation"] = consultation
        attachment_serializer = self.fields["attachments"]
        attachment_serializer.create(attachments_data)
        return consultation


class ConsultationUpdateSerializer(
    ConsultationTotalCostMixin,
    ModelBaseSerializer,
):
    """Represent serializer for update API in Consultation model."""

    total_cost = serializers.SerializerMethodField()
    created = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M",
    )
    attachments = ConsultationAttachmentSerializer(
        many=True,
        required=False,
        allow_null=True,
    )
    status = serializers.ChoiceField(
        choices=ConsultationStatus.choices,
        required=False,
    )

    class Meta:
        model = models.Consultation
        fields = (
            "id",
            "from_user",
            "to_user",
            "status",
            "created",
            "session_type",
            "attachments",
            "description",
            "note",
            "duration",
            "cost",
            "fee",
            "total_cost",
            "completed_at",
        )
        read_only_fields = (
            "from_user",
            "to_user",
            "session_type",
            "completed_at",
        )
        extra_kwargs = {
            "description": {"required": True},
        }

    def validate(self, attrs: dict) -> dict:
        """Validate if the consultation is in requested status."""
        errors = {}
        instance = self.instance
        if instance.status != ConsultationStatus.REQUESTED:
            if attrs["duration"] != instance.duration:
                errors["duration"] = _(
                    "Cannot edit duration after accept/decline.",
                )
            if attrs["cost"] != instance.cost:
                errors["cost"] = _("Cannot edit cost after accept/decline.")
            if attrs["fee"] != instance.fee:
                errors["fee"] = _("Cannot edit fee after accept/decline.")
            if attrs["description"] != instance.description:
                errors["description"] = _(
                    "Cannot edit description after accept/decline.",
                )
            if attrs.get("attachments") is not None:
                errors["attachments"] = _(
                    "Cannot edit attachments after accept/decline.",
                )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs):
        """Update consultation and its attachments."""
        status = self.validated_data.pop("status", None)
        action = CONSULTATION_STATUS_ACTION_MAP.get(status, None)
        action_method = getattr(self.instance, action) if action else None
        try:
            if action_method:
                action_method()
        except exceptions.ConsultationActionError as exc:
            raise NonFieldValidationError(exc.message) from exc
        return super().save(**kwargs)

    def update(
        self,
        instance: models.Consultation,
        validated_data: dict,
    ) -> models.Consultation:
        """Update attachments for consultation."""
        attachments_data = validated_data.pop("attachments", [])
        updated_consultation = super().update(instance, validated_data)
        if attachments_data is None:
            return updated_consultation
        updated_consultation.attachments.all().delete()
        for attachment_data in attachments_data:
            attachment_data["consultation"] = updated_consultation
        attachment_serializer = self.fields["attachments"]
        attachment_serializer.create(attachments_data)
        return updated_consultation


class ConsultationStatusSerializer(ModelBaseSerializer):
    """Represent serializer to display consultation's status."""

    class Meta:
        model = models.Consultation
        fields = (
            "id",
            "status",
        )
        extra_kwargs = {
            "status": {"read_only": True},
        }
