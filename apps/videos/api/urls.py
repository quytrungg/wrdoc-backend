from django.urls import path

from . import views

urlpatterns = [
    path(
        "auth/",
        views.VideoAuthView.as_view(),
        name="video-auth",
    ),
]
