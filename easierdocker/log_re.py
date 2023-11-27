import logging


class LogRe:
    def __init__(self, name: str = "easier-docker", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(name)s ==> %(message)s')

    def log_info(self, msg: str = ''):
        if msg == '':
            return
        self.logger.info(msg)


_logger = LogRe()
log = _logger.log_info

