from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()


def save_commands(commands_info):
    for command_info in commands_info:
        print(command_info)


def save_properties(properties_info):
    for property_info in properties_info:
        print(property_info)


def create_jobs(commands_to_call, properties_to_call):
    for key in commands_to_call.keys():
        scheduler.add_job(save_commands,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=commands_to_call[key])
    for key in properties_to_call.keys():
        scheduler.add_job(save_properties,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=properties_to_call[key])
