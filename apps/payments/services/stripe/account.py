from django.conf import settings

import stripe

from ..stripe import stripe_client


def create_account(email: str) -> stripe.Account:
    """Create Stripe Express account."""
    account = stripe_client.accounts.create(
        params={
            "type": "express",
            "country": "US",
            "email": email,
            "capabilities": {
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
        },
    )
    return account


def create_account_link(account_id: str) -> stripe.AccountLink:
    """Create Onboarding link for."""
    return stripe_client.account_links.create(
        params={
            "account": account_id,
            "return_url": settings.FRONTEND_URL,
            "refresh_url": settings.FRONTEND_URL,
            "type": "account_onboarding",
        },
    )


def get_account(account_id: str) -> stripe.Account:
    """Retrieve a Stripe account.

    Docs: https://stripe.com/docs/api/accounts/retrieve

    """
    return stripe_client.accounts.retrieve(account=account_id)
