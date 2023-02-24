"""Unit tests for logging functionality."""

import logging

from graphnet.utilities.logging import Logger, RepeatFilter
from graphnet.training.labels import Direction


# Utility function(s)
def get_number_of_lines_in_logfile(file_handler: logging.FileHandler) -> int:
    """Count and return the number of lines in log file from `FileHandler`."""
    nb_lines = 0
    with open(file_handler.baseFilename, "r") as f:
        for _ in f:
            nb_lines += 1
    return nb_lines


# Unit test(s)
def test_logging_levels() -> None:
    """Test logging calls at different levels."""
    # Construct logger and access `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 1
    file_handler = logger.file_handlers[0]

    # "Writing log to (...)"
    assert get_number_of_lines_in_logfile(file_handler) == 1

    # Debug doesn't print by default
    logger.debug("Debug")
    assert get_number_of_lines_in_logfile(file_handler) == 1

    # Info does, etc.
    logger.info("Info")
    assert get_number_of_lines_in_logfile(file_handler) == 2

    logger.warning("Warning")
    assert get_number_of_lines_in_logfile(file_handler) == 3

    logger.error("Error")
    assert get_number_of_lines_in_logfile(file_handler) == 4

    logger.critical("Critical")
    assert get_number_of_lines_in_logfile(file_handler) == 5

    # Debug prints after changing level
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug")
    assert get_number_of_lines_in_logfile(file_handler) == 6

    # Error doesn't print after changing level
    logger.setLevel(logging.CRITICAL)
    logger.error("Error")
    assert get_number_of_lines_in_logfile(file_handler) == 6

    logger.critical("Critical")
    assert get_number_of_lines_in_logfile(file_handler) == 7


def test_logging_levels_for_different_loggers() -> None:
    """Test logging calls at different levels."""
    # Construct logger and access `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 1
    file_handler = logger.file_handlers[0]

    # Construct instance that inherits from `Logger`.
    label = Direction()

    logger.info("info - root")
    label.info("info - module")
    logger.debug("debug - root")
    label.debug("debug - module")
    assert get_number_of_lines_in_logfile(file_handler) == 3

    logger.setLevel(logging.DEBUG)
    logger.debug("debug - root")
    label.debug("debug - module")
    assert get_number_of_lines_in_logfile(file_handler) == 4

    label.setLevel(logging.DEBUG)
    logger.debug("debug - root")
    label.debug("debug - module")
    assert get_number_of_lines_in_logfile(file_handler) == 6

    logger.setLevel(logging.INFO)
    logger.debug("debug - root")
    label.debug("debug - module")
    assert get_number_of_lines_in_logfile(file_handler) == 7


def test_log_folder() -> None:
    """Test logging calls at different levels."""
    # Constructing logger with no log folder shouldn't produce a `FileHandler`.
    logger = Logger(log_folder=None)
    assert len(logger.file_handlers) == 0

    # Constructing logger with a log folder, should produce a `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 1

    # Constructing logger with a new log folder, even if one has been set
    # before should produce a new `FileHandler`.
    logger = Logger(log_folder="/tmp/other_log_folder")
    assert len(logger.file_handlers) == 2

    # Constructing logger with the same log folder as before shouldn't add a
    # new `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 2


def test_logger_properties() -> None:
    """Test properties of `Logger`."""
    logger = Logger()
    assert len(logger.handlers) == 2

    # FileHandler inherits from StreamHandler
    assert len(logger.stream_handlers) == 2
    assert len(logger.file_handlers) == 1


def test_warning_once() -> None:
    """Test `Logger.warning_once` method."""
    # Construct logger and access `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 1
    file_handler = logger.file_handlers[0]
    assert get_number_of_lines_in_logfile(file_handler) == 1

    logger.warning_once("Warning")
    assert get_number_of_lines_in_logfile(file_handler) == 2

    logger.warning_once("Warning")
    assert get_number_of_lines_in_logfile(file_handler) == 2


def test_repeat_filter() -> None:
    """Test filtering of repeat messages using `RepeatFilter`."""
    # Construct logger and access `FileHandler`.
    logger = Logger()
    assert len(logger.file_handlers) == 1
    file_handler = logger.file_handlers[0]

    # Get default number of repeats allowed
    nb_repeats_allowed = RepeatFilter.nb_repeats_allowed

    # Log N-1 messages and check that they get written to file
    for ix in range(nb_repeats_allowed - 1):
        logger.info("Info")
        assert get_number_of_lines_in_logfile(file_handler) == 1 + (ix + 1)

    # Log N'th message and check that this, plus one message from the
    # `RepeatFilter` notifying that no more messages will be printed.
    logger.info("Info")
    assert get_number_of_lines_in_logfile(file_handler) == 1 + (
        nb_repeats_allowed + 1
    )

    # Log a number of additional messages and check that the output to the log
    # file doesn't change
    for ix in range(nb_repeats_allowed):
        logger.info("Info")
        assert get_number_of_lines_in_logfile(file_handler) == 1 + (
            nb_repeats_allowed + 1
        )
