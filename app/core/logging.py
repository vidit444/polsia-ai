import logging
import sys

import structlog


def configure_logging(environment: str) -> None:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]

    logging.basicConfig(
        level=logging.DEBUG if environment.lower() == "development" else logging.INFO,
        format="%(message)s",
        stream=sys.stdout,
    )
    structlog.configure(processors=processors)
