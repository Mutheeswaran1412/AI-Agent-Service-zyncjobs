import logging
import sys
from datetime import datetime
from app.config.settings import settings


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("zyncjobs_ai")
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str, **extra):
        extra_str = " | ".join(f"{k}={v}" for k, v in extra.items()) if extra else ""
        self.logger.info(f"{message}  {extra_str}" if extra_str else message)

    def error(self, message: str, **extra):
        extra_str = " | ".join(f"{k}={v}" for k, v in extra.items()) if extra else ""
        self.logger.error(f"{message}  {extra_str}" if extra_str else message)

    def warn(self, message: str, **extra):
        extra_str = " | ".join(f"{k}={v}" for k, v in extra.items()) if extra else ""
        self.logger.warning(f"{message}  {extra_str}" if extra_str else message)


logger = Logger()
