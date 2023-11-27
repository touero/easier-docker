class DockerConnectionError(Exception):
    def __init__(self, message="Unable to connect to Docker server, please make sure dockers is running."):
        self.message = message
        super().__init__(self.message)
