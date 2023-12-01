import json
import yaml

from easierdocker.log_re import log


class Config:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_file(self) -> dict:
        config = {}
        with open(self.file_path, encoding='utf8') as file:
            if self.file_path.endswith(('.yaml', '.yml')):
                config: dict = yaml.safe_load(file)
            elif self.file_path.endswith('.json'):
                config: dict = json.load(file)
            else:
                log(f'Currently unsupported file types: {self.file_path}')
        return config
