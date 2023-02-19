from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SensorDataViewSet

router = DefaultRouter()

router.register('sensordata', SensorDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
