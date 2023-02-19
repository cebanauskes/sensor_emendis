import base64
import binascii
import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sensor.models import SensorData


class GooglePubSubMessageSerializer(serializers.Serializer):
    attributes = serializers.JSONField()
    data = serializers.CharField()
    messageId = serializers.IntegerField()
    message_id = serializers.IntegerField()
    publishTime = serializers.DateTimeField()
    publish_time = serializers.DateTimeField()

    def validate_data(self, value):
        try:
            base64.b64decode(value)
            return value
        except binascii.Error:
            raise ValidationError('field data is not encoded with base64')


class GooglePubSubSerializer(serializers.Serializer):
    message = GooglePubSubMessageSerializer(required=True)
    subscription = serializers.CharField()


class SensorDataInitSerializer(serializers.Serializer):
    v0 = serializers.IntegerField()
    v18 = serializers.FloatField()
    Time = serializers.DateTimeField()


class SensorDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ('id', 'sensor_id', 'dwell_time', 'timestamp')
