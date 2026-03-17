import sys

# Access stdlib logging which is already loaded by Python/uvicorn
_logging = sys.modules["logging"]


def get_logger(name: str):
    logger = _logging.getLogger(name)
    logger.setLevel(_logging.INFO)

    if not logger.handlers:
        handler = _logging.StreamHandler()
        handler.setFormatter(_logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)

    return logger