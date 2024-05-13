# type: ignore
# pylint: disable=all

from unittest.mock import MagicMock, call, mock_open, patch

from commitlint.cli import get_args, main
from commitlint.exceptions import CommitlintException
from commitlint.messages import (
    INCORRECT_FORMAT_ERROR,
    VALIDATION_FAILED,
    VALIDATION_SUCCESSFUL,
)


class TestCLIGetArgs:
    # get_args

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(
            commit_message="commit message",
            file=None,
            hash=None,
            from_hash=None,
            quiet=None,
        ),
    )
    def test__get_args__with_commit_message(self, *_):
        args = get_args()
        assert args.commit_message == "commit message"
        assert args.file is None
        assert args.hash is None
        assert args.from_hash is None
        assert args.quiet is None

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(file="path/to/file.txt"),
    )
    def test__get_args__with_file(self, *_):
        args = get_args()
        assert args.file == "path/to/file.txt"

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(hash="commit_hash", file=None),
    )
    def test__get_args__with_hash(self, *_):
        args = get_args()
        assert args.hash == "commit_hash"
        assert args.file is None

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(from_hash="from_commit_hash", file=None, hash=None),
    )
    def test__get_args__with_from_hash(self, *_):
        args = get_args()
        assert args.from_hash == "from_commit_hash"
        assert args.file is None
        assert args.hash is None

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(
            from_hash="from_commit_hash", to_hash="to_commit_hash", file=None, hash=None
        ),
    )
    def test__get_args__with_to_hash(self, *_):
        args = get_args()
        assert args.from_hash == "from_commit_hash"
        assert args.to_hash == "to_commit_hash"
        assert args.file is None
        assert args.hash is None

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(skip_detail=True),
    )
    def test__get_args__with_skip_detail(self, *_):
        args = get_args()
        assert args.skip_detail is True


class TestCLIMain:
    # main: commit_message

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: valid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=False,
        ),
    )
    @patch("sys.stdout.write")
    def test__main__valid_commit_message(
        self,
        mock_stdout_write,
        *_,
    ):
        main()
        mock_stdout_write.assert_called_with(f"{VALIDATION_SUCCESSFUL}\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: valid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=True,
            quiet=False,
        ),
    )
    @patch("sys.stdout.write")
    def test__main__valid_commit_message_using_skip_detail(
        self,
        mock_stdout_write,
        *_,
    ):
        main()
        mock_stdout_write.assert_called_once_with(f"{VALIDATION_SUCCESSFUL}\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="Invalid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=False,
        ),
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
            [
                call("⧗ Input:\nInvalid commit message\n\n"),
                call("✖ Found 1 error(s).\n"),
                call(f"- {INCORRECT_FORMAT_ERROR}\n"),
            ]
        )

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="Invalid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=True,
            quiet=False,
        ),
    )
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__invalid_commit_message_using_skip_detail(
        self,
        mock_sys_exit,
        mock_stderr_write,
        *_,
    ):
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message\n\n"),
                call(f"{VALIDATION_FAILED}\n"),
            ]
        )

    # main: file

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", skip_detail=False, quiet=False),
    )
    @patch("sys.stdout.write")
    @patch("builtins.open", mock_open(read_data="feat: valid commit message"))
    def test__main__valid_commit_message_with_file(self, mock_stdout_write, *_):
        main()
        mock_stdout_write.assert_called_with(f"{VALIDATION_SUCCESSFUL}\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", skip_detail=False, quiet=False),
    )
    @patch("sys.stderr.write")
    @patch("sys.exit")
    @patch("builtins.open", mock_open(read_data="Invalid commit message 2"))
    def test__main__invalid_commit_message_with_file(
        self, mock_sys_exit, mock_stderr_write, *_
    ):
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message 2\n\n"),
                call("✖ Found 1 error(s).\n"),
                call(f"- {INCORRECT_FORMAT_ERROR}\n"),
            ]
        )

    # main: hash

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None, hash="commit_hash", skip_detail=False, quiet=False
        ),
    )
    @patch("commitlint.cli.get_commit_message_of_hash")
    @patch("sys.stdout.write")
    def test__main__valid_commit_message_with_hash(
        self, mock_stdout_write, mock_get_commit_message_of_hash, *_
    ):
        mock_get_commit_message_of_hash.return_value = "feat: valid commit message"
        main()
        mock_stdout_write.assert_called_with(f"{VALIDATION_SUCCESSFUL}\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None, hash="commit_hash", skip_detail=False, quiet=False
        ),
    )
    @patch("commitlint.cli.get_commit_message_of_hash")
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__invalid_commit_message_with_hash(
        self, mock_sys_exit, mock_stderr_write, mock_get_commit_message_of_hash, *_
    ):
        mock_get_commit_message_of_hash.return_value = "Invalid commit message"
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message\n\n"),
                call("✖ Found 1 error(s).\n"),
                call(f"- {INCORRECT_FORMAT_ERROR}\n"),
            ]
        )

    # main: from_hash and to_hash

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None,
            hash=None,
            from_hash="start_commit_hash",
            to_hash="end_commit_hash",
            skip_detail=False,
            quiet=False,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    @patch("sys.stdout.write")
    def test__main__valid_commit_message_with_hash_range(
        self, mock_stdout_write, mock_get_commit_messages, *_
    ):
        mock_get_commit_messages.return_value = [
            "feat: commit message 1",
            "fix: commit message 2",
        ]
        main()
        mock_stdout_write.assert_called_with(f"{VALIDATION_SUCCESSFUL}\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None,
            hash=None,
            from_hash="invalid_start_hash",
            to_hash="end_commit_hash",
            skip_detail=False,
            quiet=False,
        ),
    )
    @patch("sys.stderr.write")
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    @patch("sys.exit")
    def test__main__invalid_commit_message_with_hash_range(
        self, mock_sys_exit, mock_get_commit_messages, *_
    ):
        mock_get_commit_messages.return_value = [
            "Invalid commit message 1",
            "Invalid commit message 2",
        ]
        main()
        mock_sys_exit.assert_called_with(1)

    # main : exception handling

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(
            commit_message="feat: commit message", file=None, hash=None, from_hash=None
        ),
    )
    @patch(
        "commitlint.cli.lint_commit_message",
    )
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__handle_exceptions(
        self, mock_sys_exit, mock_stderr_write, mock_lint_commit_message, *_
    ):
        mock_lint_commit_message.side_effect = CommitlintException("Test message")
        main()
        mock_sys_exit.assert_called_with(1)
        mock_stderr_write.assert_called_with("Test message\n")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="Invalid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=True,
        ),
    )
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__quiet_option_with_invalid_commit_message(
        self, mock_sys_exit, mock_stderr_write, mock_stdout_write, *_
    ):
        main()
        mock_stderr_write.assert_not_called()
        mock_stdout_write.assert_not_called()

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: valid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=True,
        ),
    )
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    @patch("sys.exit")
    def test__main__quiet_option_with_valid_commit_message(
        self, mock_sys_exit, mock_stderr_write, mock_stdout_write, *_
    ):
        main()
        mock_stderr_write.assert_not_called()
        mock_stdout_write.assert_not_called()
        mock_sys_exit.assert_not_called()

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None,
            hash=None,
            from_hash="start_commit_hash",
            to_hash="end_commit_hash",
            skip_detail=False,
            quiet=True,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    @patch("sys.stdout.write")
    def test__valid_commit_message_with_hash_range_in_quiet(
        self, mock_stdout_write, mock_get_commit_messages, *_
    ):
        mock_get_commit_messages.return_value = [
            "feat: commit message 1",
            "fix: commit message 2",
        ]
        main()
        mock_stdout_write.assert_not_called()

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None,
            hash=None,
            from_hash="start_commit_hash",
            to_hash="end_commit_hash",
            skip_detail=False,
            quiet=True,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    @patch("sys.exit")
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    def test__invalid_commit_message_with_hash_range_in_quiet(
        self,
        mock_stderr_write,
        mock_stdout_write,
        mock_sys_exit,
        mock_get_commit_messages,
        *_,
    ):
        mock_get_commit_messages.return_value = [
            "Invalid commit message 1",
            "Invalid commit message 2",
        ]
        main()
        mock_stderr_write.assert_not_called()
        mock_sys_exit.assert_called_once_with(1)
        mock_stdout_write.assert_not_called()
