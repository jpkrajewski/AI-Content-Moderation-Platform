from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

FOLDER_ROOT = Path(__file__).parent

env = Environment(
    loader=FileSystemLoader(FOLDER_ROOT),
    autoescape=True,
)


class TemplateType(str, Enum):
    DAILY = "daily"


def get_template(template_type: TemplateType):
    return env.get_template(f"{template_type.value}.html")
