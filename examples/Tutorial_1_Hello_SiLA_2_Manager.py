"""
TUTORIAL 1: Hello_SiLA_2_Manager
---------------------------------------------

1.1 You can use this code editor like a regular scripting environment.
    If you require specific python packages for your script, you can import them here.

Hint 1: Packages you want to import must be specified in the dockerfiles requirements.txt!
    The file is located in your SiLA 2 Manager Installation directory. The default location
    on Linux is /home/<your_username>/sila2_device_manager/user_script_env/requirements.txt.
    If you change the requirements, you need to rerun the create_container.sh to update the
    docker container image.
"""
import sys
import time
import logging
import numpy as np

"""
1.2 You can use the python logging package and configure the output format here. Logging statements 
    are transferred via the stderr of the docker container and are flushed by default by the logging function.
    All output is forwarded to the SiLA 2 Manager frontend. You can display the logs in the "experiments" 
    tab by clicking on an experiment.
    When an script crashes straight-away, the logs may fail to arrive at the frontend so you have to open 
    the files directly. 
    The log files are stored locally on your computer:
    Linux:   /tmp/device_manager/container
    Windows: C:\\Users\\<your_username>\\AppData\\Local\\Temp\\device-manager\\container
"""

logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

"""
1.3 When the experiment is started, the function run() is called. Therefore, every script must 
    contain a run() function. The run function requires one argument: services. This argument 
    is used to pass the SiLA Server clients information into the script. You have to supply this
    argument, even if you don't use it!

Hint 2: Use the flush argument when using print statements or add a newline character (\n) to the 
    end of your string. Logging statements are flushed automatically.

"""


def run(services):
    """ Required to import and instantiate devices """

    print('Hello SiLA2 Manager')
    # The above print statement will not be shown in the experiment terminal before the statement below is executed and flushed.
    time.sleep(5)
    print('Yay me, i got flushed!', flush=True)
    print(f'A random number: {np.random.rand()}', flush=True)

    write_logging_statement()
    write_to_output()
"""
1.4 You can call other functions from within thr run() function. The function "write_logging_statement"
    writes logging statements of all available log_levels.
"""


def write_logging_statement():
    """Writes logging statements"""
    time.sleep(1)
    logger.debug('A debug statement')
    time.sleep(1)
    logger.info('An info statement')
    time.sleep(1)
    logger.warning('A warning statement')
    time.sleep(1)
    logger.critical('A critical warning statement')
    time.sleep(1)
    logger.error('An error statement\n')
    time.sleep(3)

"""
1.5 If direct calls to stdout and stderr are made, they won't get flushed either. Output has to be flushed explicitly.

Hint 2: Use the flush argument when using print statements and the sys.stderr.flush and sys.stdout.flush function for 
    write operations with sys.
"""


def write_to_output():
    """Writes message to stderr"""
    sys.stderr.write('Error\n')
    sys.stderr.flush()
    time.sleep(1)
    sys.stdout.write('All Good\n')
    sys.stdout.flush()
