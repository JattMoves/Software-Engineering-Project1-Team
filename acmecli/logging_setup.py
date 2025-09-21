import logging, os, sys

def configure_logging() -> None:
    log_path = os.getenv("LOG_FILE")
    level_map = { "0": logging.CRITICAL+1, "1": logging.INFO, "2": logging.DEBUG }
    level = level_map.get(os.getenv("LOG_LEVEL", "0"), logging.CRITICAL+1)
    handlers = []
    if log_path:
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    else:
        handlers.append(logging.NullHandler())
    logging.basicConfig(level=level, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
