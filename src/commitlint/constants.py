"""This module defines constants used throughout the application."""

COMMIT_HEADER_MAX_LENGTH = 72

COMMIT_TYPES = (
    "build",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "style",
    "test",
    "chore",
    "revert",
    "bump",
)

IGNORE_COMMIT_PATTERNS = (
    r"^((Merge pull request)|(Merge (.*?) into (.*?)|(Merge branch (.*?)))(?:\r?\n)*$)|"
    r"^(Merge tag (.*?))(?:\r?\n)*$|"
    r"^(R|r)evert (.*)|"
    r"^(Merged (.*?)(in|into) (.*)|Merged PR (.*): (.*))$|"
    r"^Merge remote-tracking branch(\s*)(.*)$|"
    r"^Automatic merge(.*)$|"
    r"^Auto-merged (.*?) into (.*)$|"
    r"[Bb]ump [^\s]+ from [^\s]+ to [^\s]+|"
    r"^[Ii]nitial [Cc]ommit$"
)
