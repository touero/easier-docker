import yaml


class Config:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_file(self) -> dict:
        config = {}
        if self.file_path.endswith('.yaml'):
            config: dict = yaml.load(open(self.file_path, encoding='utf8'), yaml.FullLoader)
        return config

