from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r"templates",
    views.ConsultationTemplateViewSet,
    basename="consultation-template",
)
router.register(r"", views.ConsultationViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(
        "rates/<int:user_id>",
        views.ConsultationRateAPIView.as_view(),
        name="consultation-rate",
    ),
]
