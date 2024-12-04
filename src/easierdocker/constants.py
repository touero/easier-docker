from enum import IntEnum, unique


@unique
class ContainerStatus(IntEnum):
    RUNNING = 1  # running
    EXITED = 2  # exited
    CREATED = 3  # created
