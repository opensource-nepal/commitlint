# type: ignore
# pylint: disable=all

from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from commitlint.cli import get_args, main
from commitlint.config import config
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


@patch("commitlint.console.success")
@patch("commitlint.console.error")
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
            verbose=False,
        ),
    )
    def test__main__valid_commit_message(
        self, _mock_get_args, _mock_output_error, mock_output_success
    ):
        main()
        mock_output_success.assert_called_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: valid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=True,
            quiet=False,
            verbose=False,
        ),
    )
    def test__main__valid_commit_message_using_skip_detail(
        self, _mock_get_args, _mock_output_error, mock_output_success
    ):
        main()
        mock_output_success.assert_called_once_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="Invalid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=False,
            verbose=False,
        ),
    )
    def test__main__invalid_commit_message(
        self, _mock_get_args, mock_output_error, _mock_output_success
    ):
        with pytest.raises(SystemExit):
            main()
        mock_output_error.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message\n"),
                call("✖ Found 1 error(s)."),
                call(f"- {INCORRECT_FORMAT_ERROR}"),
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
            verbose=False,
        ),
    )
    def test__main__invalid_commit_message_using_skip_detail(
        self, _mock_get_args, mock_output_error, _mock_output_success
    ):
        with pytest.raises(SystemExit):
            main()

        mock_output_error.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message\n"),
                call(f"{VALIDATION_FAILED}"),
            ]
        )

    # main: file

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", skip_detail=False, quiet=False),
    )
    @patch("builtins.open", mock_open(read_data="feat: valid commit message"))
    def test__main__valid_commit_message_with_file(
        self, _mock_get_args, _mock_output_error, mock_output_success
    ):
        main()
        mock_output_success.assert_called_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", skip_detail=False, quiet=False),
    )
    @patch(
        "builtins.open",
        mock_open(read_data="feat: valid commit message 2\n#this is a comment"),
    )
    def test__main__valid_commit_message_and_comments_with_file(
        self, _mock_get_args, _mock_output_error, mock_output_success
    ):
        main()
        mock_output_success.assert_called_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(file="path/to/file.txt", skip_detail=False, quiet=False),
    )
    @patch("builtins.open", mock_open(read_data="Invalid commit message 2"))
    def test__main__invalid_commit_message_with_file(
        self, _mock_get_args, mock_output_error, _mock_output_success
    ):
        with pytest.raises(SystemExit):
            main()

        mock_output_error.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message 2\n"),
                call("✖ Found 1 error(s)."),
                call(f"- {INCORRECT_FORMAT_ERROR}"),
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
    def test__main__valid_commit_message_with_hash(
        self,
        mock_get_commit_message_of_hash,
        _mock_get_args,
        _mock_output_error,
        mock_output_success,
    ):
        mock_get_commit_message_of_hash.return_value = "feat: valid commit message"
        main()
        mock_output_success.assert_called_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None, hash="commit_hash", skip_detail=False, quiet=False
        ),
    )
    @patch("commitlint.cli.get_commit_message_of_hash")
    def test__main__invalid_commit_message_with_hash(
        self,
        mock_get_commit_message_of_hash,
        _mock_get_args,
        mock_output_error,
        _mock_output_success,
    ):
        mock_get_commit_message_of_hash.return_value = "Invalid commit message"

        with pytest.raises(SystemExit):
            main()

        mock_output_error.assert_has_calls(
            [
                call("⧗ Input:\nInvalid commit message\n"),
                call("✖ Found 1 error(s)."),
                call(f"- {INCORRECT_FORMAT_ERROR}"),
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
            verbose=False,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    def test__main__valid_commit_message_with_hash_range(
        self,
        mock_get_commit_messages,
        _mock_get_args,
        _mock_output_error,
        mock_output_success,
    ):
        mock_get_commit_messages.return_value = [
            "feat: commit message 1",
            "fix: commit message 2",
        ]
        main()
        mock_output_success.assert_called_with(f"{VALIDATION_SUCCESSFUL}")

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file=None,
            hash=None,
            from_hash="invalid_start_hash",
            to_hash="end_commit_hash",
            skip_detail=False,
            quiet=False,
            verbose=False,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    def test__main__invalid_commit_message_with_hash_range(
        self,
        mock_get_commit_messages,
        _mock_get_args,
        _mock_output_error,
        _mock_output_success,
    ):
        mock_get_commit_messages.return_value = [
            "Invalid commit message 1",
            "Invalid commit message 2",
        ]

        with pytest.raises(SystemExit):
            main()

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
    def test__main__handle_exceptions(
        self,
        mock_lint_commit_message,
        _mock_get_args,
        mock_output_error,
        _mock_output_success,
    ):
        mock_lint_commit_message.side_effect = CommitlintException("Test message")

        with pytest.raises(SystemExit):
            main()

        mock_output_error.assert_called_with("Test message")

    # main : quiet

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: test commit",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=True,
            verbose=False,
        ),
    )
    def test__main__sets_config_for_quiet(
        self,
        _mock_get_args,
        _mock_output_error,
        _mock_output_success,
    ):
        main()
        assert config.quiet is True

    # main : verbose

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="feat: test commit",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=False,
            verbose=True,
        ),
    )
    def test__main__sets_config_for_verbose(
        self,
        _mock_get_args,
        _mock_output_error,
        _mock_output_success,
    ):
        main()
        assert config.verbose is True

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            file="path/to/non_existent_file.txt", skip_detail=False, quiet=False
        ),
    )
    def test__main__with_missing_file(
        self, _mock_get_args, _mock_output_error, mock_output_success
    ):
        mock_open().side_effect = FileNotFoundError(
            2, "No such file or directory", "path/to/non_existent_file.txt"
        )

        with pytest.raises(SystemExit):
            main()


class TestCLIMainQuiet:
    # main : quiet (directly checking stdout and stderr)

    @patch(
        "commitlint.cli.get_args",
        return_value=MagicMock(
            commit_message="Invalid commit message",
            file=None,
            hash=None,
            from_hash=None,
            skip_detail=False,
            quiet=True,
            verbose=False,
        ),
    )
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    def test__main__quiet_option_with_invalid_commit_message(
        self, mock_stderr_write, mock_stdout_write, *_
    ):
        with pytest.raises(SystemExit):
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
            verbose=False,
        ),
    )
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    def test__main__quiet_option_with_valid_commit_message(
        self, mock_stderr_write, mock_stdout_write, *_
    ):
        main()
        mock_stderr_write.assert_not_called()
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
            verbose=False,
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
            verbose=False,
        ),
    )
    @patch("commitlint.cli.get_commit_messages_of_hash_range")
    @patch("sys.stdout.write")
    @patch("sys.stderr.write")
    def test__invalid_commit_message_with_hash_range_in_quiet(
        self,
        mock_stderr_write,
        mock_stdout_write,
        mock_get_commit_messages,
        *_,
    ):
        mock_get_commit_messages.return_value = [
            "Invalid commit message 1",
            "Invalid commit message 2",
        ]

        with pytest.raises(SystemExit):
            main()

        mock_stderr_write.assert_not_called()
        mock_stdout_write.assert_not_called()
