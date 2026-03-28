"""
This module provides functions for displaying outputs related to commitlint.

NOTE: If any future changes are made to the output implementation,
they will be done from here.
"""

import sys

from .config import config

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


def red(text: str) -> str:
    return f"{RED}{text}{RESET}"


def success(message: str) -> None:
    """
    Print a success message.

    Args:
        message (str): The success message to print.
    """
    if config.quiet:
        return

    sys.stdout.write(f"{green(message)}\n")


def error(message: str) -> None:
    """
    Print an error message.

    Args:
        message (str): The error message to print.
    """
    if config.quiet:
        return

    sys.stderr.write(f"{red(message)}\n")


def verbose(message: str) -> None:
    """
    Print a verbose message if in verbose mode.

    Args:
        message (str): The verbose message to print.
    """
    if not config.verbose:
        return

    sys.stdout.write(f"{message}\n")
