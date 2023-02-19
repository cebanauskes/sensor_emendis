from django.db import models


class SensorData(models.Model):
    """Table with sensor reading"""
    sensor_id = models.PositiveIntegerField()
    dwell_time = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'sensor_data'
