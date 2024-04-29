from django.urls import include, path
from s3direct.api.views import S3DirectWrapper

app_name = "api"


urlpatterns = [
    # API URLS
    path("users/", include("apps.users.api.urls")),
    path("auth/", include("apps.users.api.auth.urls")),
    path(
        "s3/get_upload_params/",
        S3DirectWrapper.as_view(),
        name="get_s3_upload_params",
    ),
    path("constants/", include("config.urls.api_constants")),
    path("consultations/", include("apps.consultations.api.urls")),
    path("videos/", include("apps.videos.api.urls")),
    path("payments/", include("apps.payments.api.urls")),
]
