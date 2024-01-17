class DockerConnectionError(Exception):
    def __init__(self, message="Unable to connect to Docker server, please make sure dockers is running."):
        self.message = message
        super().__init__(self.message)


class NotFoundImageInDockerHub(Exception):
    def __init__(self, image_name: str):
        self.message = f'Unable to pull the image named [{image_name}], please confirm whether it exists'
        super().__init__(self.message)
