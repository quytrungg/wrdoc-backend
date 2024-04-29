from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

from apps.consultations.api.serializers import ConsultationRateSerializer
from apps.consultations.constants import TEMPLATES_COUNT
from apps.core.api.serializers import ModelBaseSerializer

from ... import services
from ..serializers import UserBaseSerializer

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.

    Copied form rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    username = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict):
        """Escape warning."""

    def update(self, instance, validated_data):
        """Escape warning."""


class TokenSerializer(OpenApiSerializer):
    """Auth token for entire app."""

    expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.REST_KNOX['TOKEN_TTL']}",
    )
    token = serializers.CharField(help_text="Token itself")
    user = UserBaseSerializer()


class PasswordResetSerializer(serializers.Serializer):
    """Request for resetting user's password."""

    information = serializers.CharField(
        help_text=_(
            "Email/Username/NPI number of account which password"
            "should be reset",
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user: User = None

    def validate_information(self, information: str) -> str:
        """Check that we have user with input email/username/NPI number."""
        query = User.objects.filter(
            Q(email=information)
            | Q(username=information)
            | Q(npi_number=information),
        )
        if not query.exists():
            raise ValidationError(
                _("There is no user with such email/username/NPI number"),
            )
        self._user = query.first()
        return information

    def create(self, validated_data: dict):
        return services.reset_user_password(self._user)

    def update(self, instance, validated_data):
        """Escape warning."""


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Request for resetting user's password.

    Explanation of token and uid

    Example `MQ-5b2-e2c1ce64d63673f0e78f`, where `MQ` - is `uid` or user id and
    `5b2-e2c1ce64d63673f0e78f` - `token` for resetting password

    """

    password = serializers.CharField(
        max_length=128,
    )
    password_confirm = serializers.CharField(
        max_length=128,
    )
    uid = serializers.CharField()
    token = serializers.CharField()
    _token_generator = PasswordResetTokenGenerator()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user: User = None

    def validate_uid(self, uid: str) -> str:
        """Validate that uid can be decoded and it's valid."""
        try:
            user_pk = force_str(urlsafe_base64_decode(uid))
        except DjangoUnicodeDecodeError as error:
            raise ValidationError(_("Invalid uid")) from error
        query = User.objects.filter(pk=user_pk)
        if not query.exists():
            raise ValidationError(_("Invalid uid"))
        self._user = query.first()
        return uid

    def validate_token(self, token: str) -> str:
        """Validate token."""
        if not self._token_generator.check_token(self._user, token):
            raise ValidationError(_("Invalid token"))
        return token

    def validate(self, attrs):
        """Validate passwords."""
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError(
                    {
                        "password_confirm": _("Passwords mismatch"),
                    },
                )
        password_validation.validate_password(password, self._user)
        return attrs

    def create(self, validated_data: dict) -> User:
        password = self.validated_data["password"]
        self._user.set_password(password)
        self._user.save()
        return self._user

    def update(self, instance, validated_data):
        """Escape warning."""


class UserRegisterSerializer(ModelBaseSerializer):
    """Serializer for user to register account."""

    password = serializers.CharField(required=True, write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)
    specialty = serializers.CharField()
    rates = ConsultationRateSerializer(
        write_only=True,
        required=False,
        many=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "entity",
            "username",
            "pronoun",
            "clinician_type",
            "specialty",
            "role",
            "npi_number",
            "credentials",
            "graduation_date",
            "primary_region_practice_state",
            "primary_region_practice_zip",
            "address_state",
            "address_zip",
            "secondary_email",
            "allow_notifications",
            "phone_number",
            "address",
            "fax_number",
            "signature",
            "rates",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "entity": {"required": False},
            "secondary_email": {"required": False},
            "phone_number": {"required": True},
            "address": {"required": True, "allow_blank": False},
            "fax_number": {"required": False},
            "signature": {"required": True, "allow_blank": False},
            "primary_region_practice_zip": {
                "required": True,
                "allow_blank": False,
            },
            "address_zip": {"required": True, "allow_blank": False},
        }

    def validate_specialty(self, specialty: str) -> list[str]:
        """Change specialty from string to list."""
        return [specialty]

    def validate_npi_number(self, npi_number: str) -> str:
        """Ensure NPI number is valid."""
        if npi_number and User.objects.filter(npi_number=npi_number).exists():
            raise ValidationError(
                _("User with this NPI number already exists"),
            )
        return npi_number

    def validate_password(self, password: str) -> str:
        """Ensure password can't contain all lowercase/uppercase letters."""
        if password.lower() == password or password.upper() == password:
            raise ValidationError(
                _("Password can't contain all lowercase/uppercase letters"),
            )
        return password

    def validate(self, attrs: dict) -> dict:
        """Validate password and `TEMPLATES_COUNT` rates if provided."""
        attrs = super().validate(attrs)
        errors = {}
        password = attrs["password"]
        password_confirm = attrs.pop("password_confirm", None)
        rates = attrs.get("rates", None)
        if rates is not None and len(rates) != TEMPLATES_COUNT:
            errors["rates"] = _(
                f"You must provide exactly {TEMPLATES_COUNT} rates",
            )
        if attrs["signature"] != f"{attrs['first_name']} {attrs['last_name']}":
            errors["signature"] = _("Signature should match with full name")
        if password != password_confirm:
            errors["password_confirm"] = _("Passwords mismatch")
        try:
            password_validation.validate_password(password, self._user)
        except ValidationError as exc:
            errors["password"] = exc.messages
        if errors:
            raise ValidationError(errors)
        return attrs

    def save(self, **kwargs) -> User:
        """Set password for user."""
        rates = self.validated_data.pop("rates", [])
        password = self.validated_data.pop("password", None)
        user = User(**self.validated_data)
        user.set_password(password)
        user.save(has_rates=bool(rates))

        for rate in rates:
            rate["user"] = user
        rate_serializer = self.fields["rates"]
        rate_serializer.create(rates)
        return user
