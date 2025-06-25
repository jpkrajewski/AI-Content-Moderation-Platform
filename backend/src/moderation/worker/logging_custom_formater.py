import datetime
import json
import logging
from typing import Any, Dict

SERVICE_NAME = "moderation"

LOG_LEVEL_MAPPING = {
    logging.DEBUG: "debug",
    logging.INFO: "info",
    logging.WARNING: "warn",
    logging.WARN: "warn",
    logging.ERROR: "error",
    logging.FATAL: "fatal",
    logging.NOTSET: "debug",
}


class CustomJsonFormatter(logging.Formatter):
    def build_log_record(self, record) -> Dict[str, Any]:
        log_record = {
            "@timestamp": datetime.datetime.utcnow().isoformat(),
            "level": LOG_LEVEL_MAPPING.get(record.levelno),
            "component": SERVICE_NAME,
            "msg": record.getMessage() if record else "",
        }
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            exc_text = exc_text.replace("\n", "")
            log_record["stackTrace"] = exc_text

        return log_record

    def format(self, record):
        log_record = self.build_log_record(record)
        return json.dumps(log_record)
