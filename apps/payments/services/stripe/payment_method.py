import stripe

from ..stripe import stripe_client


def attach_payment_method(
    customer_id: str,
    payment_method_id: str,
) -> stripe.PaymentMethod:
    """Attach a payment method to a customer."""
    attach_data: stripe.PaymentMethod.AttachParams = {"customer": customer_id}
    return stripe_client.payment_methods.attach(
        payment_method=payment_method_id,
        params=attach_data,
    )


def detach_payment_method(payment_method_id: str) -> stripe.PaymentMethod:
    """Detach a payment method from a customer, can't be reattached."""
    return stripe_client.payment_methods.detach(payment_method_id)


def list_all_payment_methods(
    list_params: stripe.PaymentMethod.ListParams | dict,
    customer_id: str = None,
) -> list[stripe.PaymentMethod]:
    """List all payment methods, can be filtered with customer."""
    if customer_id:
        list_params["customer"] = customer_id
    return stripe_client.payment_methods.list(params=list_params)
