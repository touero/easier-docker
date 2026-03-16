import unittest

from src.easierdocker.exceptions import DockerConnectionError, NotFoundImageInDockerHub


class TestExceptions(unittest.TestCase):
    def test_docker_connection_error_message(self):
        error = DockerConnectionError()

        self.assertEqual(
            str(error),
            "Unable to connect to Docker server, please make sure dockers is running.",
        )

    def test_not_found_image_in_docker_hub_message(self):
        error = NotFoundImageInDockerHub("demo-image")

        self.assertEqual(
            str(error),
            "Unable to pull the image named [demo-image], please confirm whether it exists",
        )
