from typing import Any, Dict

from moderation.worker.logging_custom_formater import CustomJsonFormatter


class WorkerJsonLogFormatter(CustomJsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            from celery._state import get_current_task

            self.get_current_task = get_current_task
        except ImportError:
            self.get_current_task = lambda: None

    def build_log_record(self, record) -> Dict[str, Any]:
        log_record = super().build_log_record(record)
        self._add_task_to_log_record(log_record)

        if not record:
            return log_record

        self._add_data_to_log_record(record=record, log_record=log_record)

        self._add_value_to_log_record(
            data=record.__dict__, log_record=log_record, data_key="funcName", record_key="method"
        )

        return log_record

    def _add_task_to_log_record(self, log_record: Dict[str, Any]):
        try:
            task = self.get_current_task()

            if not task:
                return

            log_record["task_id"] = task.request.id
            log_record["task_name"] = task.name
        except Exception:
            return

    def _add_data_to_log_record(self, record, log_record: Dict[str, Any]):
        if not record:
            return

        data = record.__dict__.get("data")

        if not data:
            return

        self._add_value_to_log_record(data=data, log_record=log_record, data_key="id", record_key="task_id")

        self._add_value_to_log_record(data=data, log_record=log_record, data_key="name", record_key="task_name")

    @staticmethod
    def _add_value_to_log_record(data: Dict[str, Any], log_record: Dict[str, Any], data_key: str, record_key: str):
        if (not data) or (log_record is None) or (not data_key) or (not record_key):
            return

        value = data.get(data_key)

        # allow zero and empty string
        if value is not None:
            log_record[record_key] = value
