#!/usr/bin/env python3
import psycopg2

def delete_user(c):
    c.execute('drop table if exists users')

def delete_devices(c):
    c.execute('drop table if exists devices')

def delete_features_for_data_handler(c):
    c.execute('drop table if exists features_for_data_handler')

def delete_commands_for_data_handler(c):
    c.execute('drop table if exists commands_for_data_handler')

def delete_properties_for_data_handler(c):
    c.execute('drop table if exists properties_for_data_handler')

def delete_parameters_for_data_handler(c):
    c.execute('drop table if exists parameters_for_data_handler')

def delete_defined_execution_errors(c):
    c.execute('drop table if exists defined_execution_errors')

def delete_databases(c):
    c.execute('drop table if exists databases')

def delete_logs(c):
    c.execute('drop table if exists log')

def delete_booking_info(c):
    c.execute('drop table if exists bookings')

def delete_experiments(c):
    c.execute('drop table if exists experiments')

def delete_scripts(c):
    c.execute('drop table if exists scripts')

def main():
    conn = psycopg2.connect(host='localhost',
                            port=5432,
                            user='postgres',
                            password='1234')
    c = conn.cursor()
    delete_user(c)
    delete_devices(c)
    delete_features_for_data_handler(c)
    delete_commands_for_data_handler(c)
    delete_properties_for_data_handler(c)
    delete_parameters_for_data_handler(c)
    delete_defined_execution_errors(c)
    delete_databases(c)
    delete_logs(c)
    delete_booking_info(c)
    delete_experiments(c)
    delete_scripts(c)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
