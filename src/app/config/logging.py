import logging
from typing import Literal
import sys

LOG_FORMAT = "%{asctime}s | %{levelname}-8s | %{name}s | %{message}s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

""" This function will be called once during application initialization. This will setup the root logger for application. """
def initialize_logger(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    root_logger = logging.getLogger("research_assistant_app")
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.propagate = False

## Get a logger for a specific component. This function returns a child logger under the `research_assistant_app` namespace.
def get_logger(component: str) -> logging.Logger:
    if not component.startswith("research_assistant_app"):
        component = f"research_assistant_app.{component}"
    return logging.getLogger(component)
