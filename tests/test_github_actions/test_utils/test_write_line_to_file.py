# type: ignore
# pylint: disable=all
from unittest.mock import mock_open, patch

from github_actions.action.utils import write_line_to_file


@patch("builtins.open", new_callable=mock_open)
def test__write_line_to_file(mock_open):
    write_line_to_file("dummy_path.txt", "Test line")

    mock_open.assert_called_once_with(file="dummy_path.txt", mode="a", encoding="utf-8")
    mock_open().write.assert_called_once_with("Test line\n")
