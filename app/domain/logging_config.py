# app/core/logging_config.py
import logging

import structlog


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),  # or ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
