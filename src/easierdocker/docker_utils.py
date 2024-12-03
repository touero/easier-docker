import time

from datetime import datetime

from docker.models.containers import Container
from .log_re import log
from .constants import ContainerStatus


def check_container_status(container: Container) -> ContainerStatus:
    for index in range(60):
        time.sleep(1)
        if container.status == ContainerStatus.CREATED.name.lower():
            continue
        if container.status != ContainerStatus.RUNNING.name.lower() and index == 0:
            container.reload()
            continue
        elif container.status == ContainerStatus.RUNNING.name.lower():
            return ContainerStatus.RUNNING
        elif container.status == ContainerStatus.EXITED.name.lower():
            log(f'Container name: [{container.name}] is exited')
            return ContainerStatus.EXITED


def check_time(target_time_str, days_ago_remove):
    """
    Check if the target_time_str is within the last days_ago_remove days
    :param target_time_str: timestamp in ISO 8601 format, accurate to nanoseconds.
    :param days_ago_remove: how many days old will the container be forcibly removed
    :return:
    """
    target_time_str = target_time_str[:26] + 'Z'
    target_time = datetime.strptime(target_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_time = datetime.utcnow()
    time_diff = current_time - target_time
    if time_diff.days >= days_ago_remove:
        return True
    return False
