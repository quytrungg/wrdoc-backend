from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VideoAppConfig(AppConfig):
    """Default configuration for Video app."""

    name = "apps.videos"
    verbose_name = _("Videos")
