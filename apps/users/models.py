from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.postgres import fields as postgres_fields
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

import citext
import stripe
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose
from localflavor.us import us_states

from apps.consultations.services import create_default_consultation_rates
from apps.core.models import BaseModel
from apps.payments.services.stripe.account import (
    create_account,
    create_account_link,
    get_account,
)

from ..payments.models import StripeAccount
from .constants import PHONE_NUMBER_LENGTH, ClinicianType, UserRole
from .querysets import UserQuerySet
from .utils import (
    default_privacy_settings,
    is_valid_npi_number,
    is_valid_phone_number,
)

US_STATES = list(us_states.US_STATES)


class UserManager(DjangoUserManager.from_queryset(UserQuerySet)):
    """Adjusted user manager that works w/o `username` field."""

    # pylint: disable=arguments-differ
    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # pylint: disable=arguments-differ
    def create_superuser(self, email, password=None, **extra_fields):
        """Create superuser instance (used by `createsuperuser` cmd)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(
    BaseModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    """Custom user model without username."""

    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=30,
        blank=True,
    )
    email = citext.CIEmailField(
        verbose_name=_("Email address"),
        max_length=254,  # to be compliant with RFCs 3696 and 5321
        unique=True,
    )
    secondary_email = citext.CIEmailField(
        verbose_name=_("Seondary Email address"),
        max_length=254,
        blank=True,
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=50,
        unique=True,
    )
    entity = models.CharField(
        verbose_name=_("Entity"),
        max_length=255,
        blank=True,
    )
    pronoun = models.CharField(
        verbose_name=_("Pronoun"),
        max_length=30,
        blank=True,
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=30,
        choices=UserRole.choices,
    )
    clinician_type = models.CharField(
        verbose_name=_("Clinician Type"),
        max_length=50,
        choices=ClinicianType.choices,
    )
    specialty = postgres_fields.ArrayField(
        verbose_name=_("Specialty"),
        base_field=models.CharField(
            max_length=255,
        ),
        default=list,
        size=3,
    )
    specialty_area = models.CharField(
        verbose_name=_("Specialty Area"),
        max_length=255,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Decline reason"),
        max_length=1024,
        blank=True,
    )
    course_schedule = models.FileField(   # noqa: DJ01
        verbose_name=_("Course Schedule"),
        max_length=1000,
        blank=True,
        null=True,
    )
    npi_number = models.CharField(
        verbose_name=_("NPI Number"),
        max_length=10,
        blank=True,
    )
    graduation_date = models.DateField(
        verbose_name=_("Graduation Date"),
        blank=True,
        null=True,
    )
    primary_region_practice_state = models.CharField(
        verbose_name=_("Primary Region of Practice State"),
        max_length=20,
        choices=US_STATES,
    )
    primary_region_practice_zip = models.CharField(
        verbose_name=_("Primary Region of Practice Zipcode"),
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(^[0-9]{5}(?:-[0-9]{4})?$|^$)",
                message=_("Valid zip code should be XXXXX or XXXXX-XXXX"),
            ),
        ],
    )
    address_state = models.CharField(
        verbose_name=_("Address State"),
        max_length=20,
        choices=US_STATES,
    )
    address_zip = models.CharField(
        verbose_name=_("Address Zipcode"),
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(^[0-9]{5}(?:-[0-9]{4})?$|^$)",
                message=_("Valid zip code should be XXXXX or XXXXX-XXXX"),
            ),
        ],
    )
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=10,
        blank=True,
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=255,
        blank=True,
    )
    fax_number = models.CharField(
        verbose_name=_("Fax Number"),
        max_length=10,
        blank=True,
    )
    allow_notifications = models.BooleanField(
        verbose_name=_("Allow Notifications"),
        default=False,
    )
    signature = models.TextField(
        verbose_name=_("Signature"),
        blank=True,
        default="",
    )
    credentials = models.CharField(
        verbose_name=_("Credentials"),
        max_length=255,
        blank=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active.",
        ),
    )

    avatar = imagekitmodels.ProcessedImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    avatar_thumbnail = imagekitmodels.ImageSpecField(
        source="avatar",
        processors=[
            ResizeToFill(50, 50),
        ],
    )
    privacy_settings = models.JSONField(
        default=default_privacy_settings,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        # pylint: disable=invalid-str-returned
        return self.email

    def save(self, has_rates=False, *args, **kwargs) -> None:
        """Create default rates if user is created without providing rates."""
        super().save(*args, **kwargs)
        if not has_rates and self.rates.count() == 0:
            create_default_consultation_rates(self)

    def clean_npi_number(self) -> None:
        """Ensure `npi_number` is a string of 10 numbers."""
        if self.npi_number and not is_valid_npi_number(self.npi_number):
            raise ValidationError(
                _(f"NPI number must be {PHONE_NUMBER_LENGTH} digits long."),
            )

    def clean_phone_number(self) -> None:
        """Ensure `phone_number` is a string of 10 numbers."""
        if self.phone_number and not is_valid_phone_number(self.phone_number):
            raise ValidationError(
                _(f"Phone number must be {PHONE_NUMBER_LENGTH} digits long."),
            )

    def clean_fax_number(self) -> None:
        """Ensure `fax_number` is a string of 10 numbers."""
        if self.fax_number and not is_valid_phone_number(self.fax_number):
            raise ValidationError(
                _(f"Fax number must be {PHONE_NUMBER_LENGTH} digits long."),
            )

    def clean_email(self) -> None:
        """Ensure email is unique throughout the system."""
        if User.objects.filter(
            secondary_email=self.email,
        ).exclude(id=self.pk).exists():
            raise ValidationError(_("User with this email already exists."))

    def clean_secondary_email(self) -> None:
        """Ensure `secondary_email` is different from `email`."""
        if self.secondary_email and User.objects.filter(
            Q(email=self.secondary_email)
            | Q(secondary_email=self.secondary_email),
        ).exclude(id=self.pk).exists():
            raise ValidationError(_("User with this email already exists."))

    def clean(self) -> None:
        """Provide validations between multiple fields in User."""
        super().clean()
        errors = {}
        if self.role == UserRole.CLINICIAN and not self.npi_number:
            errors["npi_number"] = _("Clinician must provide NPI number.")
        if self.email == self.secondary_email:
            err_msg = _("Secondary email and primary email must be different.")
            errors["email"] = err_msg
            errors["secondary_email"] = err_msg
        if errors:
            raise ValidationError(errors)

    def get_stripe_account(self) -> stripe.Account:
        """Fetch linked Stripe Account."""
        stripe_account = StripeAccount.objects.filter(user=self).first()
        if stripe_account:
            return get_account(stripe_account.stripe_id)
        account = create_account(self.email)
        StripeAccount(stripe_id=account.stripe_id, user=self).save()
        return account

    def get_account_link(self) -> stripe.AccountLink:
        """Generate Stripe Account Link."""
        account = self.get_stripe_account()
        account_link = create_account_link(account_id=account["id"])
        return account_link


class Contact(BaseModel):
    """Represent contact list for user."""

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("User who owns the contact"),
        related_name="contacts",
    )
    contact = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("User who is set as contact for owner"),
        related_name="contact_of",
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        unique_together = ("owner", "contact")

    def __str__(self):
        return f"Contact of {self.owner_id} - {self.contact_id}"
