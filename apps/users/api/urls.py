from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

# register URL like
# router.register(r"users", UsersAPIView)
router = DefaultRouter()
router.register(r"profile", views.UserProfileViewSet, basename="profile")
router.register(r"contact", views.ContactViewSet, basename="contact")
router.register(r"", views.UsersViewSet, basename="user")

urlpatterns = [
    path(
        "profile/",
        views.UserProfileRetrieveUpdateViewSet.as_view(
            {"get": "list", "put": "update", "patch": "partial_update"},
        ),
        name="profile",
    ),
]
urlpatterns += router.urls
