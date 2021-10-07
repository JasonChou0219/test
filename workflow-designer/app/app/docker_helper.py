import logging
import docker
import subprocess
import ctypes, sys
from time import sleep, time
from docker.errors import DockerException

from LHS_scheduler_service.source.setup.generate_config import config
from LHS_scheduler_service.source.setup.config import settings


logging.getLogger(__name__)
image_dict: dict = {
    'Database-redis': {'name': config['Database-redis']['name'], 'version': config['Database-redis']['version'], 'image': config['Database-redis']['image']},
    'Database-postgres': {'name': config['Database-postgres']['name'], 'version': config['Database-postgres']['version'], 'image': config['Database-postgres']['image']},
    'Database-influxdb': {'name': config['Database-influxdb']['name'], 'version': config['Database-influxdb']['version'],'image': config['Database-influxdb']['image']},
}


def get_docker_client():
    return docker.from_env()


def is_docker_running():
    """Check if the docker server is running"""
    try:
        get_docker_client().ping()
        return True
    except DockerException as e:
        logging.warning('Docker is not running!')
        return False


def is_docker_installed():
    """Check whether docker is installed by using a subprocess call or an API call"""
    try:
        version = subprocess.check_output(['docker', '--version'])
        print(f'Docker is installed: {str(version, "utf-8")}')
        return True
    except FileNotFoundError as e:
        logging.warning('Docker is not installed!')
        return False


def start_docker():
    """Start the docker daemon service"""
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(['powershell.exe', 'restart-service', '*docker*']), None, 1 )
        #subprocess.run('powershell.exe restart-service *docker*')
    except Exception as e:
        print(e)
        logging.error('Could not start docker service!')
        raise UserWarning


def download_docker_images():
    for container_app in image_dict.keys():
        logging.info(f'Downloading image {container_app}')
        get_docker_client().images.pull(repository=image_dict[container_app]['image'], tag=image_dict[container_app]['version'])


def create_postgres_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)
    if settings.POSTGRES_DB in container_list:
        delete_postgres_container()
    get_docker_client().containers.create(image=f'{settings.POSTGRES_IMAGE}:{settings.POSTGRES_VERSION}',
                                          command=None,
                                          name=settings.POSTGRES_DB,
                                          environment=[f'POSTGRES_PASSWORD={settings.POSTGRES_PASSWORD}', f'POSTGRES_USER={settings.POSTGRES_USER}'],
                                          ports={'5432/tcp': settings.POSTGRES_PORT},
                                          user=settings.POSTGRES_USER)


def create_redis_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)
    if settings.REDIS_DB in container_list:
        delete_redis_container()
    get_docker_client().containers.create(image=f'{settings.REDIS_IMAGE}:{settings.REDIS_VERSION}',
                                          command=None,
                                          name=settings.REDIS_DB,
                                          ports={'6379/tcp': settings.REDIS_PORT},
                                          user=settings.REDIS_USER)


def create_influxdb_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)
    if settings.INFLUX_DB in container_list:
        delete_influxdb_container()
    get_docker_client().containers.create(image=f'{settings.INFLUX_IMAGE}:{settings.INFLUX_VERSION}',
                                          command=None,
                                          name=settings.INFLUX_DB,
                                          ports={'8086/tcp': (settings.INFLUX_HOST, settings.INFLUX_PORT)},
                                          environment=[f'INFLUX_USERNAME={settings.INFLUX_USER}',
                                                       f'INFLUX_PASSWORD={settings.INFLUX_PASSWORD}'])


def run_postgres_container():
    create_postgres_container()
    start_postgres_container()


def run_redis_container():
    create_redis_container()
    start_redis_container()


def run_influxdb_container():
    create_influxdb_container()
    start_influxdb_container()


def start_postgres_container():
    container = get_docker_client().containers.get(container_id=settings.POSTGRES_DB)
    container.start()
    wait_until_ready_postgres()


def start_redis_container():
    container = get_docker_client().containers.get(container_id=settings.REDIS_DB)
    container.start()
    wait_until_ready_redis()


def start_influxdb_container():
    container = get_docker_client().containers.get(container_id=settings.INFLUX_DB)
    container.start()
    wait_until_ready_influx()


def wait_until_ready_postgres(timeout: float = 60):
    t_start = time()
    response: str = ''
    sleep_interval = 0.2
    while time() <= (t_start + timeout):
        try:
            response = str(subprocess.check_output(['docker', 'exec', image_dict['Database-postgres']['name'], 'pg_isready']), 'utf-8')
            if 'accepting connections' in response:
                logging.info(str('Postgres alive:'+str(response)))
                return True
            elif 'Error response from daemon'in response:
                sleep(sleep_interval)
            else:
                sleep(sleep_interval)
        except subprocess.CalledProcessError:
            pass
    logging.error(f'Timeout for postgres database reached.')
    return False


def wait_until_ready_redis(timeout: float = 60):
    t_start = time()
    response: str = ''
    sleep_interval = 0.2
    while time() <= (t_start + timeout):
        try:
            response = str(subprocess.check_output(['docker', 'exec', image_dict['Database-redis']['name'], 'redis-cli', 'PING']), 'utf-8')
            if 'PONG' in response:
                logging.info(str('Redis alive:'+str(response)))
                return True
            else:
                sleep(sleep_interval)
        except subprocess.CalledProcessError:
            pass
    logging.error(f'Timeout for redis database reached.')
    return False


def wait_until_ready_influx(timeout: float = 60):
    t_start = time()
    response: str = ''
    sleep_interval = 0.2
    while time() <= (t_start + timeout):
        try:
            response = subprocess.check_output(['curl', '-sL', '-I', f'{settings.INFLUX_HOST}:{settings.INFLUX_PORT}/ping'], shell=True, encoding='utf-8')  #, universal_newlines=True)
            if '204 No Content' in response:
                logging.info(str('InfluxDB alive:'+str(response)))
                return True
            else:
                sleep(sleep_interval)
        except subprocess.CalledProcessError:
            pass
    logging.error(f'Timeout for influx database reached.')
    return False


def postgres_container_is_running() -> bool:
    status = get_docker_client().containers.get(settings.POSTGRES_DB).status
    if status == 'running':
        return True
    else:
        return False


def redis_container_is_running() -> bool:
    status = get_docker_client().containers.get(settings.REDIS_DB).status
    if status == 'running':
        return True
    else:
        return False


def influxdb_container_is_running() -> bool:
    status = get_docker_client().containers.get(settings.INFLUX_DB).status
    if status == 'running':
        return True
    else:
        return False


def stop_postgres_container():
    container = get_docker_client().containers.get(container_id=settings.POSTGRES_DB)
    container.stop(timeout=5)


def stop_redis_container():
    container = get_docker_client().containers.get(container_id=settings.REDIS_DB)
    container.stop(timeout=5)


def stop_influxdb_container():
    container = get_docker_client().containers.get(container_id=settings.INFLUX_DB)
    container.stop(timeout=5)


def delete_postgres_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)

    if settings.POSTGRES_DB in container_list:
        if postgres_container_is_running():
            stop_postgres_container()
        container = get_docker_client().containers.get(container_id=settings.POSTGRES_DB)
        container.remove(v=True, force=True)


def delete_redis_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)
    if settings.REDIS_DB in container_list:
        if redis_container_is_running():
            stop_redis_container()
        container = get_docker_client().containers.get(container_id=settings.REDIS_DB)
        container.remove(v=True, force=True)


def delete_influxdb_container():
    container_list = []
    for container in get_docker_client().containers.list(all=True):
        container_list.append(container.name)
    if settings.INFLUX_DB in container_list:
        if influxdb_container_is_running():
            stop_influxdb_container()
        container = get_docker_client().containers.get(container_id=settings.INFLUX_DB)
        container.remove(v=True, force=True)


def delete_postgres_image():
    if f'{settings.POSTGRES_IMAGE}:{settings.POSTGRES_VERSION}' in get_docker_client().images.list():
        if postgres_container_is_running():
            stop_postgres_container()
            delete_postgres_container()
        get_docker_client().images.remove(image=f'{settings.POSTGRES_IMAGE}:{settings.POSTGRES_VERSION}', force=True)


def delete_redis_image():
    if f'{settings.REDIS_IMAGE}:{settings.REDIS_VERSION}' in get_docker_client().images.list():
        if redis_container_is_running():
            stop_redis_container()
            delete_redis_container()
        get_docker_client().images.remove(image=f'{settings.REDIS_IMAGE}:{settings.REDIS_VERSION}', force=True)


def delete_influxdb_image():
    if f'{settings.INFLUX_IMAGE}:{settings.INFLUX_VERSION}' in get_docker_client().images.list():
        if influxdb_container_is_running():
            stop_influxdb_container()
            delete_influxdb_container()
        get_docker_client().images.remove(image=f'{settings.INFLUX_IMAGE}:{settings.INFLUX_VERSION}', force=True)


def delete_docker_containers():
    delete_postgres_container()
    delete_influxdb_container()
    delete_redis_container()
    return 0


def delete_docker_images():
    delete_postgres_image()
    delete_redis_image()
    delete_influxdb_image()


def container_startup_dialogue_redis():
    if not redis_container_is_running():
        i = 0
        while i <= 3:
            response = input('Docker: Redis container not running. Start redis docker container? [Y/n]')
            if response in ['n', 'N']:
                logging.warning('Docker: Not starting container!')
                break
            elif response in ['y', 'Y', '']:
                if not redis_container_is_running():
                    start_redis_container()
                sleep(2)
                if redis_container_is_running():
                    logging.info('Docker: Redis container is running...')
                    break
                else:
                    i += 1
                    if i == 3:
                        logging.error('Docker: Could not start Redis!')
                        raise DockerException
            else:
                i += 1
                if i == 3:
                    logging.error('Invalid input!')
                    raise DockerException
    else:
        logging.info('Docker: Redis container is running...')


def container_startup_dialogue_postgres():
    if not postgres_container_is_running():
        i = 0
        while i <= 3:
            response = input('Docker: PostgreSQL container not running. Start postgreSQL docker container? [Y/n]')
            if response in ['n', 'N']:
                logging.warning('Docker: Not starting container!')
                break
            elif response in ['y', 'Y', '']:
                if not postgres_container_is_running():
                    start_postgres_container()
                sleep(2)
                if postgres_container_is_running():
                    logging.info('Docker: PostgreSQL container is running...')
                    break
                else:
                    i += 1
                    if i == 3:
                        logging.error('Docker: Could not start PostgreSQL!')
                        raise DockerException
            else:
                i += 1
                if i == 3:
                    logging.error('Invalid input!')
                    raise DockerException

    else:
        logging.info('Docker: PostgreSQL container is running...')


def container_startup_dialogue_influxdb():
    if not influxdb_container_is_running():
        i = 0
        while i <= 3:
            response = input('Docker: InfluxDB container not running. Start InfluxDB docker container? [Y/n]')
            if response in ['n', 'N']:
                logging.warning('Docker: Not starting container!')
                break
            elif response in ['y', 'Y', '']:
                if not influxdb_container_is_running():
                    start_influxdb_container()
                sleep(2)
                if influxdb_container_is_running():
                    logging.info('Docker: InfluxDB container is running...')
                    break
                else:
                    i += 1
                    if i == 3:
                        logging.error('Docker: Could not start InfluxDB!')
                        raise DockerException
            else:
                i += 1
                if i == 3:
                    logging.error('Invalid input!')
                    raise DockerException
    else:
        logging.info('Docker: InfluxDB container is running...')
