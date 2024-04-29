from apps.users.api import views as user_views
from apps.consultations.api import views as consultation_views
from django.urls import path


urlpatterns = [
    path(
        "state-choices",
        user_views.StateChoiceAPIView.as_view(),
        name="state-choice",
    ),
    path(
        "clinician-choices",
        user_views.ClinicianChoiceAPIView.as_view(),
        name="clinician-choice",
    ),
    path(
        "specialty-choices",
        user_views.SpecialtyChoiceAPIView.as_view(),
        name="specialty-choice",
    ),
    path(
        "session-types",
        consultation_views.SessionTypeChoiceAPIView.as_view(),
        name="session-type",
    ),
    path(
        "privacy-choice",
        user_views.PrivacyChoiceAPIView.as_view(),
        name="privacy-choice",
    ),
]
