import datetime

from sensor.models import SensorData


def create(sensor_id: int, dwell_time: float, timestamp: datetime) -> SensorData:
    """Create sensor readings object"""
    return SensorData.objects.create(
        sensor_id=sensor_id,
        dwell_time=dwell_time,
        timestamp=timestamp
    )
