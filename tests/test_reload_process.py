import sys
import unittest
from unittest.mock import patch

from src.easierdocker.reload_process import reload_process


class TestReloadProcess(unittest.TestCase):
    @patch("src.easierdocker.log_re.log")
    @patch("os.execl")
    def test_reload_process_reexecutes_current_process(self, mock_execl, mock_log):
        with patch.object(sys, "argv", ["reload_process.py", "--debug"]):
            reload_process("/usr/bin/python3", "python", "/tmp/app.py")

        mock_log.assert_called_once_with(
            "Reloading process with /usr/bin/python3 python /tmp/app.py ['--debug']"
        )
        mock_execl.assert_called_once_with("/usr/bin/python3", "python", "/tmp/app.py", "--debug")
