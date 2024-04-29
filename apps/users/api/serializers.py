# pylint: disable=abstract-method
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from s3direct.api.fields import S3DirectUploadURLField

from apps.consultations.api.serializers.consultation_rate import (
    ConsultationRateSerializer,
)
from apps.consultations.constants import TEMPLATES_COUNT
from apps.core.api.serializers import BaseSerializer, ModelBaseSerializer
from apps.users.constants import PrivacyFields, PrivacyOptions
from apps.users.models import Contact, User


class UserBaseSerializer(ModelBaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "avatar",
            "clinician_type",
            "entity",
            "specialty",
        )


class UserListSerializer(UserBaseSerializer):
    """Serializer for list of users."""

    has_contact = serializers.BooleanField(read_only=True)
    total_contacts = serializers.IntegerField(read_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "specialty_area",
            "has_contact",
            "total_contacts",
        )


class UserDetailSerializer(ModelBaseSerializer):
    """Represent serializer for user profile."""

    avatar = S3DirectUploadURLField(allow_null=True)
    has_contact = serializers.SerializerMethodField()
    total_contacts = serializers.SerializerMethodField()
    rates = ConsultationRateSerializer(
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "avatar",
            "first_name",
            "last_name",
            "username",
            "entity",
            "pronoun",
            "credentials",
            "clinician_type",
            "graduation_date",
            "email",
            "secondary_email",
            "phone_number",
            "address",
            "primary_region_practice_state",
            "primary_region_practice_zip",
            "address_state",
            "address_zip",
            "fax_number",
            "description",
            "specialty",
            "specialty_area",
            "created",
            "has_contact",
            "total_contacts",
            "rates",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "primary_region_practice_zip": {"required": True},
            "address_zip": {"required": True},
        }

    def get_has_contact(self, user: User) -> bool:
        """Return whether the user has contact."""
        if hasattr(user, "has_contact"):
            return user.has_contact
        request = self.context.get("request")
        # Omit check on privacy settings serialization
        if not request:
            return True
        logged_user = request.user
        return logged_user.contacts.filter(contact=user).exists()

    def get_total_contacts(self, user: User) -> int:
        """Return total contacts for the user."""
        if hasattr(user, "total_contacts"):
            return user.total_contacts
        request = self.context.get("request")
        # Omit check on privacy settings serialization
        if not request:
            return 0
        return user.contacts.count()

    def validate(self, attrs) -> dict:
        """Ensure user only provides `TEMPLATES_COUNT` rates to update."""
        attrs = super().validate(attrs)
        rates = attrs.get("rates", None)
        if rates is not None and len(rates) != TEMPLATES_COUNT:
            raise serializers.ValidationError(
                {
                    "rates": _(
                        f"You must provide exactly {TEMPLATES_COUNT} rates.",
                    ),
                },
            )
        return attrs

    def update(self, instance: User, validated_data) -> User:
        """Update user's profile."""
        updated_rates = validated_data.pop("rates", None)
        updated_instance = super().update(instance, validated_data)

        if updated_rates is None:
            return updated_instance

        rate_serializer = self.fields["rates"]
        rate_serializer.update(updated_instance.rates.all(), updated_rates)
        return updated_instance


class ContactSerializer(ModelBaseSerializer):
    """Serializer for Contact model."""

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Contact
        fields = (
            "owner",
            "contact",
        )


class UserListField(serializers.ListField):
    """Provide user's name and id for representation."""

    child = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def to_representation(self, data) -> list[dict]:
        """Convert user's id to id-to-name mapping."""
        users = User.objects.filter(id__in=data)
        return [UserDetailSerializer(instance=user).data for user in users]

    def to_internal_value(self, data) -> list[int]:
        """Return just list of ints."""
        return data


class PrivacyFieldSerializer(BaseSerializer):
    """Serializer for privacy setting."""

    type = serializers.ChoiceField(choices=PrivacyOptions, required=True)
    users = UserListField(allow_empty=True, required=True)

    def validate(self, attrs):
        """Check that users exist."""
        users = attrs["users"]

        if attrs["type"] == PrivacyOptions.CUSTOM and (
            not users or not User.objects.filter(id__in=users).exists()
        ):
            raise serializers.ValidationError("Incorrect user ID was passed.")

        return attrs


class PrivacySettingsSerializer(BaseSerializer):
    """Serializer for user's Privacy Settings."""

    about_me = PrivacyFieldSerializer(required=True)
    speciality = PrivacyFieldSerializer(required=True)
    practice_area = PrivacyFieldSerializer(required=True)

    def update(self, instance: User, validated_data) -> dict:
        for privacy_field in PrivacyFields.values:
            instance.privacy_settings[privacy_field] = {
                "type": validated_data[privacy_field]["type"],
                "users": validated_data[privacy_field]["users"],
            }
        instance.save(update_fields=("privacy_settings",))
        return instance.privacy_settings


class ResponsePrivacySettingsSerializer(BaseSerializer):
    """Serializer for user's Privacy Settings only for spec."""

    about_me = serializers.DictField()
    speciality = serializers.DictField()
    practice_area = serializers.DictField()
    education = serializers.DictField()
    rating = serializers.DictField()


class DashboardSerializer(BaseSerializer):
    """Serializer for displaying user's dashboard."""

    consultation_count = serializers.IntegerField()
    request_count = serializers.IntegerField()
    earnings = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        coerce_to_string=False,
    )
