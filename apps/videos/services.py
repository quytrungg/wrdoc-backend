from time import time

from django.conf import settings

import jwt

from .constants import VIDEO_EXP_TIME_EPOCH


def generate_video_jwt_signature(payload_data: dict) -> str:
    """Generate JWT signature for Zoom video."""
    iat = int(time())
    exp = iat + VIDEO_EXP_TIME_EPOCH

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "app_key": settings.ZOOM_VIDEO_APP_KEY,
        "version": 1,
        "iat": iat,
        "exp": exp,
        **payload_data,
    }
    payload["role_type"] = int(payload["role_type"])

    signature = jwt.encode(
        headers=header,
        payload=payload,
        key=settings.ZOOM_VIDEO_SECRET_KEY,
        algorithm="HS256",
    )
    return signature
