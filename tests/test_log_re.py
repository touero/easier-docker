import unittest
from unittest.mock import MagicMock, patch

from src.easierdocker.log_re import LogRe


class TestLogRe(unittest.TestCase):
    @patch("src.easierdocker.log_re.logging.basicConfig")
    @patch("src.easierdocker.log_re.logging.getLogger")
    def test_log_info_ignores_empty_message(self, mock_get_logger, mock_basic_config):
        logger = MagicMock()
        mock_get_logger.return_value = logger
        log_re = LogRe()

        self.assertIs(log_re.logger, logger)
        log_re.log_info("")

        mock_basic_config.assert_called_once()
        logger.info.assert_not_called()

    @patch("src.easierdocker.log_re.logging.getLogger")
    def test_log_info_writes_message(self, mock_get_logger):
        logger = MagicMock()
        mock_get_logger.return_value = logger
        log_re = LogRe(name="custom-name")

        log_re.log_info("hello")

        logger.info.assert_called_once_with("hello")
