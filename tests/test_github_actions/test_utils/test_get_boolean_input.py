# type: ignore
# pylint: disable=all
import os
from unittest.mock import patch

import pytest

from github_actions.action.utils import get_boolean_input


@patch.dict(os.environ, {"INPUT_TEST": "True"})
def test__get_boolean_input__return_True_for_True():
    assert get_boolean_input("test") is True


@patch.dict(os.environ, {"INPUT_TEST": "TRUE"})
def test__get_boolean_input__return_True_for_TRUE():
    assert get_boolean_input("test") is True


@patch.dict(os.environ, {"INPUT_TEST": "true"})
def test__get_boolean_input__return_True_for_true():
    assert get_boolean_input("test") is True


@patch.dict(os.environ, {"INPUT_TEST": "False"})
def test__get_boolean_input__return_False_for_False():
    assert get_boolean_input("test") is False


@patch.dict(os.environ, {"INPUT_TEST": "FALSE"})
def test__get_boolean_input__return_False_for_FALSE():
    assert get_boolean_input("test") is False


@patch.dict(os.environ, {"INPUT_TEST": "false"})
def test__get_boolean_input__return_False_for_false():
    assert get_boolean_input("test") is False


@patch.dict(os.environ, {"INPUT_TEST": "random"})
def test__get_boolean_input__raises_type_error_for_unknown():
    with pytest.raises(TypeError):
        get_boolean_input("test")
