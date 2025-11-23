"""
Contains config for the commitlint.
"""

from typing import Optional

from .constants import COMMIT_HEADER_MAX_LENGTH


class _CommitlintConfig:
    """
    Singleton class for storing commitlint configs
    """

    _instance: Optional["_CommitlintConfig"] = None  # for singleton property

    _verbose: bool = False
    _quiet: bool = False
    _max_header_length: int = COMMIT_HEADER_MAX_LENGTH

    def __new__(cls) -> "_CommitlintConfig":
        """
        Return singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def verbose(self) -> bool:
        """
        Get the current verbose setting.

        Returns:
            bool: The current verbose setting.
        """
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        """
        Set the verbose setting.

        Args:
            value (bool): New value for verbose setting.
        """
        if value:
            self._quiet = False

        self._verbose = value

    @property
    def quiet(self) -> bool:
        """
        Get the current quiet setting.

        Returns:
            bool: The current quiet setting.
        """
        return self._quiet

    @quiet.setter
    def quiet(self, value: bool) -> None:
        """
        Set the quiet setting.

        Args:
            value (bool): New value for quiet setting.
        """
        if value:
            self._verbose = False

        self._quiet = value

    @property
    def max_header_length(self) -> int:
        """
        Get the current max_header_length setting.
        Returns:
            int: The current max_header_length setting.
        """
        return self._max_header_length

    @max_header_length.setter
    def max_header_length(self, value: int) -> None:
        """
        Set the max_header_length setting.
        Args:
            value (int): New value for max_header_length setting.
        """
        self._max_header_length = value


config = _CommitlintConfig()

__all__ = [
    "config",
]
