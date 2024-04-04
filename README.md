# commitlint

[![PyPI version](https://badge.fury.io/py/commitlint.svg)](https://badge.fury.io/py/commitlint)
[![CI status](https://github.com/opensource-nepal/commitlint/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/opensource-nepal/commitlint/actions)
[![Downloads](https://img.shields.io/pypi/dm/commitlint.svg?maxAge=180)](https://pypi.org/project/commitlint/)
[![codecov](https://codecov.io/github/opensource-nepal/commitlint/graph/badge.svg?token=lRmPZsIHb6)](https://codecov.io/github/opensource-nepal/commitlint)
[![License](https://img.shields.io/pypi/l/commitlint?label=License)](https://github.com/opensource-nepal/commitlint/blob/main/LICENSE)

commitlint is a tool designed to lint your commit messages according to the [Conventional Commits](https://www.conventionalcommits.org/) standard for your pre-commit hook and GitHub Actions.

## How to use

### For pre-commit

1. Add the following configuration on `.pre-commit-config.yaml`.

   ```yaml
   repos:
   ...

   - repo: https://github.com/opensource-nepal/commitlint
       rev: v0.2.1
       hooks:
       - id: commitlint

   ...
   ```

2. Install the `commit-msg` hook in your project repo:

   ```bash
   pre-commit install --hook-type commit-msg
   ```

> **_NOTE:_** Installing using only `pre-commit install` will not work.

### For github-actions

If you have any existing workflows, add the following steps:

```yaml
...
steps:
    ...
    - name: Run commitlint
    uses: opensource-nepal/commitlint@v0.2.1
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
      - uses: actions/checkout@v4

      - name: Run commitlint
        uses: opensource-nepal/commitlint@v0.2.1
```

> **_NOTE:_** commitlint GitHub Actions will only be triggered by "push" or "pull_request" events.

#### GitHub Action Inputs

| #   | Name              | Type    | Default | Description                                                           |
| --- | ----------------- | ------- | ------- | --------------------------------------------------------------------- |
| 1   | **fail_on_error** | Boolean | true    | Determines whether the GitHub Action should fail if commitlint fails. |

#### GitHub Action Outputs

| #   | Name          | Type    | Description                                                                  |
| --- | ------------- | ------- | ---------------------------------------------------------------------------- |
| 1   | **exit_code** | Integer | The exit code of the commitlint step.                                        |
| 2   | **status**    | String  | The outcome of the commitlint step. Possible values: 'success' or 'failure'. |


## CLI (Command Line Interface)

### Help Example
```shell
$ commitlint --help
usage: commitlint [-h] [-V] [--file FILE] [--hash HASH] [--from-hash FROM_HASH] [--to-hash TO_HASH] [--skip-detail] [commit_message]

Check if a commit message follows the conventional commit format.

positional arguments:
  commit_message        The commit message to be checked.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --file FILE           Path to a file containing the commit message.
  --hash HASH           Commit hash
  --from-hash FROM_HASH
                        From commit hash
  --to-hash TO_HASH     To commit hash
  --skip-detail         Skip the detailed error message check
```

### Usage Examples
Check commit message directly:
 
```shell
$ commitlint "chore: my commit message"
```

Check commit message from file:

```shell
$ commitlint --file /foo/bar/commit-message.txt
```

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

Version check:

```shell
$ commitlint --version
# or
$ commitlint -V
```

## Contribution

We appreciate feedback and contribution to this package. To get started please see our [contribution guide](./CONTRIBUTING.md).
