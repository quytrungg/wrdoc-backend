import typing

import stripe

from ..stripe import stripe_client

if typing.TYPE_CHECKING:
    from apps.users.models import User


def create_customer(user: "User") -> stripe.Customer:
    """Create a new customer."""
    return stripe_client.customers.create(
        params={
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "phone": user.phone_number,
        },
    )


def retrieve_customer(customer_id: str) -> stripe.Customer:
    """Retrieve a customer."""
    return stripe_client.customers.retrieve(customer=customer_id)
