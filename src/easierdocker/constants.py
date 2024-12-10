from enum import IntEnum, unique
from dataclasses import dataclass, fields
from typing import Dict


@unique
class ContainerStatus(IntEnum):
    RUNNING = 1  # running
    EXITED = 2  # exited
    CREATED = 3  # created


@dataclass
class ExtraConfigModel:
    is_remove: int
    days_ago_remove: int
    remove_now: int

    @staticmethod
    def validate_dict(config_dict: Dict):
        allowed_fields = {field.name: field.type for field in fields(ExtraConfigModel)}
        for key, value in config_dict.items():
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: '{key}' in extra_config")

            expected_type = allowed_fields[key]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Field '{key}' expects type '{expected_type.__name__}', but got '{type(value).__name__}'")
