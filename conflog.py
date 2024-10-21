import logging
import json
from time import strftime, localtime
import os


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(CustomJsonFormatter, self).format(record)
        log_time = strftime("%Y-%m-%d %H:%M", localtime())
        log_dict = {"time": log_time, "levelname": record.levelname, "message": record.message}
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
