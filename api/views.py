import base64
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, response, status, mixins
from rest_framework.filters import OrderingFilter

import sensor.services
from api.permissions import IsJWTAuthorized
from api.serializers import SensorDataInitSerializer, SensorDataListSerializer, \
    GooglePubSubSerializer
from sensor.models import SensorData


class SensorDataViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    permission_classes = (IsJWTAuthorized,)
    queryset = SensorData.objects.order_by('id')
    serializer_class = SensorDataListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('sensor_id', 'dwell_time',)
    ordering_fields = ('id', 'timestamp', 'dwell_time')

    def create(self, request, *args, **kwargs):
        """Create sensor reading data from Google pub/sub message"""
        pub_sub_serializer = GooglePubSubSerializer(data=request.data)
        pub_sub_serializer.is_valid(raise_exception=True)
        sensor_serializer = SensorDataInitSerializer(
            data=json.loads(
                base64.b64decode(
                    pub_sub_serializer.validated_data['message']['data']
                )
            )
        )
        sensor_serializer.is_valid(raise_exception=True)
        sensor.services.create(
            sensor_id=sensor_serializer.validated_data['v0'],
            dwell_time=sensor_serializer.validated_data['v18'],
            timestamp=sensor_serializer.validated_data['Time']
        )
        return response.Response(status=status.HTTP_201_CREATED)

