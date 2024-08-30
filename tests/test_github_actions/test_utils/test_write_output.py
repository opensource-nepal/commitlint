# type: ignore
# pylint: disable=all
import os
from unittest.mock import mock_open, patch

from github_actions.action.utils import write_output


@patch("builtins.open", new_callable=mock_open)
def test__write_output(mock_open):
    with patch.dict(os.environ, {"GITHUB_OUTPUT": "output.txt"}):
        write_output("key", "value")

        mock_open.assert_called_once_with(file="output.txt", mode="a", encoding="utf-8")
        mock_open().write.assert_called_once_with("key=value\n")
