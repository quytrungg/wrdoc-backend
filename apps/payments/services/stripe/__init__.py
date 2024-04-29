# pylint: disable=wrong-import-position
from django.conf import settings

import stripe as stripe_api

stripe_client = stripe_api.StripeClient(
    api_key=settings.STRIPE_API_KEY,
    http_client=stripe_api.RequestsClient(),
)
