from django.conf import settings

import stripe
from requests.compat import urljoin

from ..stripe import stripe_client


def create_checkout_session() -> str:
    """Create a checkout session for user."""
    return_url = urljoin(
        base=settings.FRONTEND_URL,
        url="checkout/return?session_id={CHECKOUT_SESSION_ID}",
    )
    session = stripe_client.checkout.sessions.create(
        params={
            "payment_method_types": ["card"],
            "mode": "setup",
            "ui_mode": "embedded",
            "return_url": return_url,
        },
    )
    return session.client_secret


def create_checkout_session_payment(
    connected_account_id,
    session_type: str,
    amount: int,
    fee: int,
) -> stripe.checkout.Session:
    """Create Checkout Session in Stripe."""
    return stripe_client.checkout.sessions.create(
        params={
            "line_items": [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": session_type},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                },
            ],
            "payment_intent_data": {
                "application_fee_amount": fee,
                "transfer_data": {"destination": connected_account_id},
                "capture_method": "manual",
            },
            "mode": "payment",
            "ui_mode": "embedded",
            "return_url": f"checkout/return?session_id={connected_account_id}",
        },
    )


def retrieve_checkout_session(session_id: str) -> stripe.checkout.Session:
    """Retrieve a checkout session."""
    return stripe_client.checkout.sessions.retrieve(session_id)


def retrieve_setup_intent(setup_intent_id: str) -> stripe.SetupIntent:
    """Retrieve a setup intent."""
    return stripe_client.setup_intents.retrieve(setup_intent_id)
