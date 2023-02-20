## Available methods
| endpoint | request type | description |
| :--- | :--- | :--- | 
| api/v1/sensordata/?sensor_id=&?dwell_time= | GET| Getting a list of sensordata with optional filters|
| api/v1/sensordata/ | POST | Create sensor data in db|

## Instructions for launching project
1. Clone repository ('https://github.com/cebanauskes/sensor_emendis.git')
2. Create python virtualenv (`python3 -m venv venv`)
3. Launch virtualenv (`source venv/bin/activate`) on Mac/Linux ir (`source venv/Scripts/activate`) on Windows
4. Install all required packages, that are specified in file requirements.txt (`pip install -r requirements.txt`)
5. Create file ".env" and add write SENSOR_JWT_SECRET
6. Launch django migrations (`python manage.py migrate`)
6. For launching the server write the following command in terminal (`python manage.py runserver`)
