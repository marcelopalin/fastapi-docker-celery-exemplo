import logging
from pathlib import Path

from app.src.custom_logging import CustomizeLogger

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("logging_config.json")
logger = CustomizeLogger.make_logger(config_path)
