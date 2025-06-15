from abc import ABC, abstractmethod
from typing import Any, Dict


class EmailClient(ABC):
    @abstractmethod
    def send(self, email_params: Dict[str, Any]) -> bool: ...
