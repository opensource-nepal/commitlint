# type: ignore
# pylint: disable=all
import os
import pytest
from unittest.mock import patch

from github_actions.action.utils import get_int_input


def test__get_int_input__parses_positive_int():
    with patch.dict(os.environ, {"INPUT_TEST": "1"}):
        assert get_int_input("test") == 1


def test__get_int_input__parses_negative_int():
    with patch.dict(os.environ, {"INPUT_TEST": "-1"}):
        assert get_int_input("test") == -1


def test__get_int_input__returns_none_if_empty():
    # GitHub Action passes empty data as a empty string ("")
    with patch.dict(os.environ, {"INPUT_TEST": ""}):
        assert get_int_input("test") is None


def test__get_int_input__raises_exception_if_float():
    with patch.dict(os.environ, {"INPUT_TEST": "2.5"}):
        with pytest.raises(ValueError):
            get_int_input("test")


def test__get_int_input__raises_exception_if_str():
    with patch.dict(os.environ, {"INPUT_TEST": "hello"}):
        with pytest.raises(ValueError):
            get_int_input("test")
