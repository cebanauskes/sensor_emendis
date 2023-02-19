import jwt
from django.conf import settings

from rest_framework.permissions import BasePermission


class IsJWTAuthorized(BasePermission):
    message = "Provide sensor-token in request headers"

    def has_permission(self, request, view):
        token = request.headers.get('sensor-token')
        return token and jwt.decode(
            token,
            settings.SENSOR_JWT_SECRET,
            algorithms=["HS256"]
        )
