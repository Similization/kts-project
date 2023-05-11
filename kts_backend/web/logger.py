import logging
import typing

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


def setup_logging(
    app: "Application", log_file: str = None, log_level: str = "INFO"
) -> None:
    """
    Set up logging for the application.

    Args:
        app: An instance of the Application class.
        log_file: The file name for the log file. If not provided, logs will be written to console.
        log_level: The level of logging to be used (e.g., "INFO", "DEBUG", "WARNING", etc.). Defaults to "INFO".
    """
    log_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if log_file:
        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setFormatter(log_formatter)
        app.logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.getLevelName(log_level))
