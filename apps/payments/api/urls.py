from django.urls import path

from . import views

urlpatterns = [
    path(
        "checkout-session/",
        views.CheckoutSessionAPIView.as_view(),
        name="checkout-session",
    ),
    path(
        "attach-payment/",
        views.AttachPaymentMethodAPIView.as_view(),
        name="attach-payment",
    ),
]
