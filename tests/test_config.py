# type: ignore
# pylint: disable=all

from typing import Generator

import pytest

from commitlint.config import _CommitlintConfig as CommitlintConfig


@pytest.fixture(scope="class")
def config_instance() -> Generator[CommitlintConfig, None, None]:
    config = CommitlintConfig()
    yield config
    config.verbose = False
    config.quiet = False


class TestCommitlintConfig:
    def test_singleton_instance(self, config_instance: CommitlintConfig) -> None:
        config1 = config_instance
        config2 = config_instance
        assert config1 is config2

    def test_verbose_property(self, config_instance: CommitlintConfig) -> None:
        config = config_instance
        config.verbose = True
        assert config.verbose
        assert not config.quiet

    def test_quiet_property(self, config_instance: CommitlintConfig) -> None:
        config = config_instance
        config.quiet = True
        assert config.quiet
        assert not config.verbose
