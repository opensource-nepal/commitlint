"""
Contains config for the commitlint.
"""

from typing import Optional


class _CommitlintConfig:
    """
    Singleton class for storing commitlint configs
    """

    _instance: Optional["_CommitlintConfig"] = None  # for singleton property

    _verbose: bool = False
    _quiet: bool = False

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


config = _CommitlintConfig()

__all__ = [
    "config",
]
