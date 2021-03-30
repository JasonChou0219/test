"""
TUTORIAL 4: Incorporating Databases
---------------------------------------------
4.1 Import the InfluxDBClient and other packages you will need
"""
from influxdb import InfluxDBClient
from datetime import datetime
import numpy as np
import time

"""
4.2 Instantiate the InfluxDBClient with the connection details of the respective database and check the connection by 
    pinging the database server. Make sure to change the default connection details below to your database details!
"""


def run(services):
    influx_client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='SiLA_2_Manager')
    print(f'Checking connectivity. DB server version: {influx_client.ping()}', flush=True)

    """
    4.3 If you do not already have a database, creat a new one:
    """

    influx_client.create_database(dbname='SiLA_2_Manager')

    """
    4.4 Create a datapoint to write to the database. Add adequate tags so you can filter your data efficiently in 
        chronograf. If your script is running, you can check your data live in your browser, if your chronograf server 
        is running: <ip-of-the-chronograf/influxDB-server>:8888 .
    """

    for i in range(0, 25, 1):
        # This is an example write operation
        random_number = np.random.rand()
        data_point = {
            "measurement": "testMeasurement",
            "tags": {
                "experiment_name": "influxDB_test",
                "device": "experiment_docker_container"
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "test_number": random_number
            }
        }

        try:
            influx_client.write_points([data_point])
            print(f'A random number was written to the database: {random_number}', flush=True)
        except:
            print("This did not work...")

        """
        4.5 Query your data using the SQL-like Influx Query Language (InfluxQL). You can find information on the syntax at:
            https://docs.influxdata.com/influxdb/v1.8/query_language/ . The following query will read the value that was 
            just written to the database.
        
        Hint 4: Copy and paste the query below to visualize the data in chronograf. Change the LIMIT to display the 
            number of last data points. Remove the escape character (backslash) around the influxDB_test in the query. 
            You can leave out the last part of the query, starting at ORDER BY, to display all available measurements 
            of this type.
        """

        # This is an example query.
        results = influx_client.query(
            'SELECT test_number FROM "SiLA_2_Manager"."autogen"."testMeasurement" WHERE experiment_name = \'influxDB_test\' GROUP BY position ORDER BY DESC LIMIT 1')
        print('The latest random number was queried from the database: ',  flush=True)
        print(results, flush=True)
        time.sleep(5)
