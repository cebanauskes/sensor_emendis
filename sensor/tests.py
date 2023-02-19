import json
import jwt
from datetime import datetime

from django.conf import settings
from rest_framework.test import APITestCase

from sensor.models import SensorData


class BaseClientCase(APITestCase):
    def setUp(self) -> None:
        self.token = jwt.encode({'payload': 'payload'}, settings.SENSOR_JWT_SECRET, algorithm='HS256')


class TestListSensorData(BaseClientCase):
    def setUp(self) -> None:
        super().setUp()
        self.sensor_data_1 = SensorData.objects.create(sensor_id=1, dwell_time=12.12, timestamp=datetime.now())
        self.sensor_data_2 = SensorData.objects.create(sensor_id=23, dwell_time=12.12, timestamp=datetime.now())

    def test_list(self):
        response = self.client.get(
            '/api/v1/sensordata/',
            HTTP_SENSOR_TOKEN=str(self.token)

        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filtered_list(self):
        response = self.client.get(
            f'/api/v1/sensordata/?sensor_id={self.sensor_data_1.sensor_id}',
            HTTP_SENSOR_TOKEN=str(self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class TestCreateSensorData(BaseClientCase):
    def test_create(self):
        """Test creating sensor data object with correct data"""
        response = self.client.post(
            '/api/v1/sensordata/',
            HTTP_SENSOR_TOKEN=str(self.token),
            data=json.dumps({
                "message": {
                    "attributes": {
                        "key": "value"
                    },
                    "data": "eyJzZXJpYWwiOiAiMDAwMTAwMDAwMTAwIiwgImFwcGxpY2F0aW9uIjogMTEsICJUaW1lIjogIjIwMjItMTEtMDhUMDQ6MDA6MDQuMzE3ODAxIiwgIlR5cGUiOiAieGtndyIsICJkZXZpY2UiOiAiVGVzdERldmljZSIsICJ2MCI6IDEwMDAxMywgInYxIjogMC42OSwgInYyIjogMS4zMSwgInYzIjogMC4xOCwgInY0IjogMCwgInY1IjogMC44LCAidjYiOiAwLCAidjciOiAyNjk2NSwgInY4IjogMC4xLCAidjkiOiA5Nzc1NzQ5NiwgInYxMCI6IDAsICJ2MTEiOiAwLCAidjEyIjogMS44NCwgInYxMyI6IDAsICJ2MTQiOiAwLjcsICJ2MTUiOiAxMDAxMCwgInYxNiI6IDEwMDAxMywgInYxNyI6IDI2OTY1LCAidjE4IjogMi43Mn0=",
                    "messageId": "2070443601311540",
                    "message_id": "2070443601311540",
                    "publishTime": "2021-02-26T19:13:55.749Z",
                    "publish_time": "2021-02-26T19:13:55.749Z"
                },
                "subscription": "projects/myproject/subscriptions/mysubscription"

            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(SensorData.objects.all())

    def test_create_wrong_data_type(self):
        """Test creating with wrong base64 encoded field"""
        response = self.client.post(
            '/api/v1/sensordata/',
            HTTP_SENSOR_TOKEN=str(self.token),
            data=json.dumps({
                "message": {
                    "attributes": {
                        "key": "value"
                    },
                    "data": "Wrong data",
                    "messageId": "2070443601311540",
                    "message_id": "2070443601311540",
                    "publishTime": "2021-02-26T19:13:55.749Z",
                    "publish_time": "2021-02-26T19:13:55.749Z"
                },
                "subscription": "projects/myproject/subscriptions/mysubscription"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


