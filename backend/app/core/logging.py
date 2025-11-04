import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
ch.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:
    logger.addHandler(ch)
