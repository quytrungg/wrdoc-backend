from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentAppConfig(AppConfig):
    """Default app config for payments app.

    This app include stripe and payment related models
    and services.

    """

    name = "apps.payments"
    verbose_name = _("Payments")
