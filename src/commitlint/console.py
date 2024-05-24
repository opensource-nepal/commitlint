"""
This module provides functions for displaying outputs related to commitlint.

NOTE: If any future changes are made to the output implementation,
they will be done from here.

TODO: Add color on success and error (#5).
"""

import sys

from .config import config


def success(message: str) -> None:
    """
    Print a success message.

    Args:
        message (str): The success message to print.
    """
    if config.quiet:
        return

    sys.stdout.write(f"{message}\n")


def error(message: str) -> None:
    """
    Print an error message.

    Args:
        message (str): The error message to print.
    """
    if config.quiet:
        return

    sys.stderr.write(f"{message}\n")


def verbose(message: str) -> None:
    """
    Print a verbose message if in verbose mode.

    Args:
        message (str): The verbose message to print.
    """
    if not config.verbose:
        return

    sys.stdout.write(f"{message}\n")
