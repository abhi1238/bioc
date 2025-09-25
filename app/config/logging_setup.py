import logging

def setup_logging_uvicorn_style(loglevel="INFO", logfile="biochirp.log"):
    """
    Ensures all logs go through the 'uvicorn.error' logger and also to a file.
    """
    logger = logging.getLogger("uvicorn.error")
    logger.setLevel(getattr(logging, loglevel.upper(), logging.INFO))

    # Only add file handler if not already present (avoid duplicates on reload)
    if logfile:
        file_handler_exists = any(
            isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == logfile
            for h in logger.handlers
        )
        if not file_handler_exists:
            file_handler = logging.FileHandler(logfile, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
