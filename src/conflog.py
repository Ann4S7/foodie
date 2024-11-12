import json
import logging
import os
from time import localtime, strftime


class CustomJsonFormatter(logging.Formatter):
    """Determine the output formatting of log messages."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log message.

        Args:
            record: a log.

        Returns: json string that contains the log message.

        """
        super().format(record)
        log_time = strftime("%Y-%m-%d %H:%M", localtime())
        log_dict = {
            "time": log_time,
            "levelname": record.levelname,
            "message": record.message,
        }
        if hasattr(record, "extra_parameters"):
            log_dict.update(record.extra_parameters)

        return json.dumps(log_dict, default=str)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if os.environ.get("ENV") == "TEST":
    handler = logging.StreamHandler()
else:
    handler = logging.FileHandler("logs.json")

file_formatter = CustomJsonFormatter()
handler.setFormatter(file_formatter)
logger.addHandler(handler)
