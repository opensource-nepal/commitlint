# Commitlint CLI

## Installation

```shell
pip install commitlint
```

## Usage

```
commitlint [-h] [-V] [--file FILE] [--hash HASH] [--from-hash FROM_HASH] [--to-hash TO_HASH] [--skip-detail] [--hide-input]
           [-q | -v]
           [commit_message]

Check if a commit message follows the Conventional Commits format.

Positional arguments:
  commit_message        The commit message to be checked.

Options:
  -h, --help            Show this help message and exit.
  -V, --version         Show the program's version number and exit.
  --file FILE           Path to a file containing the commit message.
  --hash HASH           Commit hash.
  --from-hash FROM_HASH Commit hash to start checking from.
  --to-hash TO_HASH     Commit hash to check up to.
  --skip-detail         Skip detailed error messages.
  --hide-input          Hide input from stdout.
  -q, --quiet           Suppress stdout and stderr.
  -v, --verbose         Enable verbose output.
```

## Examples

Check a commit message directly:

```shell
$ commitlint "chore: my commit message"
```

Check a commit message from a file:

```shell
$ commitlint --file /foo/bar/commit-message.txt
```

> **_Note:_** When using the `--file` option, avoid commit messages that start with `#`, as this may cause unexpected behavior with `commitlint`.

Check the commit message of a specific hash:

```shell
$ commitlint --hash 9a8c08173
```

Check commit messages within a hash range:

```shell
$ commitlint --from-hash 00bf73fef7 --to-hash d6301f1eb0
```

Check a commit message while skipping detailed error messages:

```shell
$ commitlint --skip-detail "chore: my commit message"
# or
$ commitlint --skip-detail --hash 9a8c08173
```

Run `commitlint` in quiet mode:

```shell
$ commitlint --quiet "chore: my commit message"
```

Run `commitlint` in verbose mode:

```shell
$ commitlint --verbose "chore: my commit message"
```

Check the version:

```shell
$ commitlint --version
# or
$ commitlint -V
```
