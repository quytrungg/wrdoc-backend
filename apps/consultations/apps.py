from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConsultationAppConfig(AppConfig):
    """Default configuration for Consultation app."""

    name = "apps.consultations"
    verbose_name = _("Consultations")
