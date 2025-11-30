import logging
from pathlib import Path
from datetime import datetime


def setup_logging():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"log_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    return log_file

def write_info_log(log_message):
    logging.info(log_message)

def write_warning_log(log_message):
    logging.warning(log_message)

def write_error_log(log_message):
    logging.error(log_message)

def write_critical_log(log_message):
    logging.critical(log_message)