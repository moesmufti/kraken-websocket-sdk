import logging


def setup_logging(level=logging.INFO):
    """
    Sets up basic logging with a file handler.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Define formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File Handler - logs all levels DEBUG and above
    file_handler = logging.FileHandler("kraken_ws.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Stream Handler - Optional: Uncomment if you want logs on the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if setup_logging is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)  # Uncomment if needed
