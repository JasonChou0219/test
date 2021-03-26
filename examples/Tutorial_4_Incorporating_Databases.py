from influxdb import InfluxDBClient
from datetime import datetime
import numpy as np
import time

# Instantiate the database client.
influx_client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='device_manager')

# Check connection
print(f'Checking connectivity. DB server version: {influx_client.ping()}')

for i in range(0, 100, 1):
    # This is an example write operation
    data_point = {
        "measurement": "testMeasurement",
        "tags": {
            "experiment_name": "influxDB_test"
        },
        "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fields": {
            "test_number": np.random.rand(1)
        }
    }

    try:
        influx_client.write_points([data_point])
    except:
        print("This did not work...")

    # This is an example query.
    results = influx_client.query(
        'SELECT test_number FROM "device_manager"."autogen"."testMeasurement" WHERE experiment_name = \'influxDB_test\' GROUP BY position'
        'ORDER BY DESC LIMIT 1')
    print(results)

    time.sleep(10)
