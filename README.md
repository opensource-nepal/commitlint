# commitlint

[![PyPI version](https://badge.fury.io/py/commitlint.svg)](https://badge.fury.io/py/commitlint)
[![CI status](https://github.com/opensource-nepal/commitlint/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/opensource-nepal/commitlint/actions)
[![Downloads](https://img.shields.io/pypi/dm/commitlint.svg?maxAge=180)](https://pypi.org/project/commitlint/)
[![codecov](https://codecov.io/github/opensource-nepal/commitlint/graph/badge.svg?token=lRmPZsIHb6)](https://codecov.io/github/opensource-nepal/commitlint)
[![License](https://img.shields.io/pypi/l/commitlint?label=License)](https://github.com/opensource-nepal/commitlint/blob/main/LICENSE)

commitlint is a tool designed to lint your commit messages according to the [Conventional Commits](https://www.conventionalcommits.org/) standard for your pre-commit hook and GitHub Actions.

## Conventional Commits

A conventional commit message follows a specific format that includes a prefix indicating the type of change, an optional scope for context, and a concise description of the modification.
This structure improves readability, facilitates automated changelog generation, and ensures a consistent commit history.

The commit message should follow this structure:

```
<type>(<optional scope>): <description>

[Optional body]
```

**Type:** Indicates the type of change, such as build, ci, docs, feat, fix, perf, refactor, style, test, chore, revert, or bump.
E.g., `feat: add JSON parser`.

**Scope:** Additional contextual information.
E.g., `feat(parser): add JSON parser`.

**Description:** Brief description of the commit.

**Body:** A detailed description of the commit.

For more details, please refer to the Conventional Commits specification at https://www.conventionalcommits.org/en/v1.0.0/

> NOTE: commitlint also checks the length of the commit header (**max 72 characters**). The commit header refers to the first line of the commit message (excluding the body).

## How to use

### For pre-commit

1. Add the following configuration on `.pre-commit-config.yaml`.

   ```yaml
   repos:
      ...
      - repo: https://github.com/opensource-nepal/commitlint
        rev: v1.0.0
        hooks:
          - id: commitlint
      ...
   ```

2. Install the `commit-msg` hook in your project repo:

   ```bash
   pre-commit install --hook-type commit-msg
   ```

   Installing using only `pre-commit install` will not work.

> **_NOTE:_** Avoid using commit messages that start with '#'.
> This might result in unexpected behavior with commitlint.

### For GitHub Actions

If you have any existing workflows, add the following steps:

```yaml
...
steps:
    ...
    - name: Run commitlint
      uses: opensource-nepal/commitlint@v1
    ...
```

If you don't have any workflows, create a new GitHub workflow, e.g. `.github/workflows/commitlint.yaml`.

```yaml
name: Commitlint

on:
  push:
    branches: ['main']
  pull_request:

jobs:
  commitlint:
    runs-on: ubuntu-latest
    name: Commitlint
    steps:
      - name: Run commitlint
        uses: opensource-nepal/commitlint@v1
```

> **_NOTE:_** commitlint GitHub Actions will only be triggered by "push", "pull_request", or "pull_request_target" events. The difference between "pull_request" and "pull_request_target" is that "pull_request" is more secure for public repos while "pull_request_target" is necessary for private repos.

#### GitHub Action Inputs

| #   | Name              | Type    | Default | Description                                                           |
| --- | ----------------- | ------- | ------- | --------------------------------------------------------------------- |
| 1   | **fail_on_error** | Boolean | true    | Determines whether the GitHub Action should fail if commitlint fails. |
| 2   | **verbose**       | Boolean | false   | Verbose output.                                                       |

#### GitHub Action Outputs

| #   | Name          | Type    | Description                                                                  |
| --- | ------------- | ------- | ---------------------------------------------------------------------------- |
| 1   | **exit_code** | Integer | The exit code of the commitlint step.                                        |
| 2   | **status**    | String  | The outcome of the commitlint step. Possible values: 'success' or 'failure'. |

## CLI (Command Line Interface)

### Installation

```shell
pip install commitlint
```

### Usage

```
commitlint [-h] [-V] [--file FILE] [--hash HASH] [--from-hash FROM_HASH] [--to-hash TO_HASH] [--skip-detail] [-q | -v]
           [commit_message]

positional arguments:
  commit_message        The commit message to be checked

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --file FILE           Path to a file containing the commit message
  --hash HASH           Commit hash
  --from-hash FROM_HASH
                        From commit hash
  --to-hash TO_HASH     To commit hash
  --skip-detail         Skip the detailed error message check
  -q, --quiet           Ignore stdout and stderr
  -v, --verbose         Verbose output
```

### Examples

Check commit message directly:

```shell
$ commitlint "chore: my commit message"
```

Check commit message from file:

```shell
$ commitlint --file /foo/bar/commit-message.txt
```

> **_NOTE:_** For `--file` option, avoid using commit messages that start with '#'.
> This might result in unexpected behavior with commitlint.

Check commit message of a hash:

```shell
$ commitlint --hash 9a8c08173
```

Check commit message of a hash range:

```shell
$ commitlint --from-hash 00bf73fef7 --to-hash d6301f1eb0
```

Check commit message skipping the detail check:

```shell
$ commitlint --skip-detail "chore: my commit message"
# or
$ commitlint --skip-detail --hash 9a8c08173
```

Run commitlint in quiet mode:

```shell
$ commitlint --quiet "chore: my commit message"
```

Run commitlint in verbose mode:

```shell
$ commitlint --verbose "chore: my commit message"
```

Version check:

```shell
$ commitlint --version
# or
$ commitlint -V
```

## Contribution

We appreciate feedback and contribution to this package. To get started please see our [contribution guide](./CONTRIBUTING.md).
