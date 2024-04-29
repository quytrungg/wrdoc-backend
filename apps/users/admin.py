from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from ..core.admin import BaseAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""

    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "username",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "email",
                    "username",
                    "secondary_email",
                    "password",
                    "role",
                ),
            },
        ),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "entity",
                    "pronoun",
                    "clinician_type",
                    "specialty",
                    "npi_number",
                    "credentials",
                    "graduation_date",
                    "phone_number",
                    "primary_region_practice_state",
                    "primary_region_practice_zip",
                    "address",
                    "address_state",
                    "address_zip",
                    "fax_number",
                    "avatar",
                ),
            },
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
