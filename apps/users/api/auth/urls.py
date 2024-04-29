from django.urls import path

from knox import views as knox_views

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path(
        "logout-all/", knox_views.LogoutAllView.as_view(),
        name="logout-all",
    ),
    path(
        "password-reset/", views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset-confirm/", views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
