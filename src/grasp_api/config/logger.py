import json
import logging
import sys


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }
        return json.dumps(log_record)


logger = logging.getLogger("grasp_api")
logger.setLevel(logging.INFO)

console_formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

json_formatter = JSONFormatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(console_formatter)

file_handler = logging.FileHandler("logs/app.jsonl")
file_handler.setFormatter(json_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
