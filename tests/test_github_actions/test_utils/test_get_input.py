# type: ignore
# pylint: disable=all
import os
from unittest.mock import patch

from github_actions.action.utils import get_input


def test_get_input_variable_set():
    with patch.dict(os.environ, {"INPUT_TEST": "value"}):
        assert get_input("test") == "value"
