# type: ignore
# pylint: disable=all

from unittest.mock import MagicMock, call, mock_open, patch

from src.commitlint.cli import get_args, main
from src.commitlint.messages import COMMIT_SUCCESSFUL, INCORRECT_FORMAT_ERROR


class TestCLI:
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(commit_message="commit message", file=None),
    )
    def test__get_args__with_commit_message(self, *_):
        args = get_args()
        assert args.commit_message == "commit message"
        assert args.file is None

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(commit_message=None, file="path/to/file.txt"),
    )
    def test__get_args__with_file(self, *_):
        args = get_args()
        assert args.file == "path/to/file.txt"
        assert args.commit_message is None

    @patch("argparse.ArgumentParser.error")
    def test__get_args__without_commit_message_and_file(self, mock_error):
        get_args()
        mock_error.assert_called_with(
            "Please provide either a commit message or a file."
        )

    @patch(
        "src.commitlint.cli.get_args",
        return_value=MagicMock(commit_message="feat: valid commit message", file=None),
    )
    @patch("sys.stdout.write")
    @patch("sys.exit")
    def test__main__valid_commit_message(
        self,
        mock_sys_exit,
        mock_stdout_write,
        *_,
    ):
        main()
        mock_sys_exit.assert_called_with(0)
        mock_stdout_write.assert_called_with(f"{COMMIT_SUCCESSFUL}\n")

    @patch(
        "src.commitlint.cli.get_args",
        return_value=MagicMock(commit_message="Invalid commit message", file=None),
    )
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__invalid_commit_message(
        self,
        mock_sys_exit,
        mock_stderr_write,
        *_,
    ):
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_has_calls(
            [call("✖ Found 1 errors.\n\n"), call(f"- {INCORRECT_FORMAT_ERROR}\n\n")]
        )

    @patch(
        "src.commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", commit_message=None),
    )
    @patch("sys.stdout.write")
    @patch("sys.exit")
    @patch("builtins.open", mock_open(read_data="feat: valid commit message"))
    def test__main__valid_commit_message_from_file(
        self, mock_sys_exit, mock_stdout_write, *_
    ):
        main()
        mock_sys_exit.assert_called_with(0)
        mock_stdout_write.assert_called_with(f"{COMMIT_SUCCESSFUL}\n")

    @patch(
        "src.commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", commit_message=None),
    )
    @patch("sys.stderr.write")
    @patch("sys.exit")
    @patch("builtins.open", mock_open(read_data="Invalid commit message"))
    def test__main__invalid_commit_message_from_file(
        self, mock_sys_exit, mock_stderr_write, *_
    ):
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_has_calls(
            [call("✖ Found 1 errors.\n\n"), call(f"- {INCORRECT_FORMAT_ERROR}\n\n")]
        )
