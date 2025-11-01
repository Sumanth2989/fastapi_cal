import logging
import sys

def configure_logging(level: str = "INFO") -> None:
    # Root logger configuration
    logger = logging.getLogger()
    if logger.handlers:
        # Avoid duplicate handlers in reloads
        return
    logger.setLevel(level)

    handler = logging.StreamHandler(stream=sys.stdout)
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
