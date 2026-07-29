"""Module for AppParams"""

from dataclasses import dataclass


@dataclass
class AppParams:
    """
    Represents runtime parameters that control linting behavior and output handling.

    These parameters are typically derived from CLI arguments and define how
    commit messages are validated and displayed.
    """

    # Skips the detailed error check (fails immediately without detail error message).
    skip_detail: bool = False

    # Hide input from stdout/stderr. Specifically used by GitHub Actions.
    hide_input: bool = False

    # Maximum header length to check. If not specified, the header length is not checked.
    max_header_length: int | None = None

    # Remove comments from the commit message.
    strip_comments: bool = False
