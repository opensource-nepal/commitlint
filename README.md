# Conventional Commitlint

[![PyPI version](https://badge.fury.io/py/commitlint.svg)](https://badge.fury.io/py/commitlint)
[![CI status](https://github.com/opensource-nepal/commitlint/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/opensource-nepal/commitlint/actions)
[![Downloads](https://img.shields.io/pypi/dm/commitlint.svg?maxAge=180)](https://pypi.org/project/commitlint/)
[![codecov](https://codecov.io/github/opensource-nepal/commitlint/graph/badge.svg?token=lRmPZsIHb6)](https://codecov.io/github/opensource-nepal/commitlint)
[![License](https://img.shields.io/pypi/l/commitlint?label=License)](https://github.com/opensource-nepal/commitlint/blob/main/LICENSE)

`commitlint` is a tool that lints commit messages according to the [Conventional Commits](./docs/conventional-commits.md) standard. It can be used in GitHub Actions and as a pre-commit hook.

## Usage

### GitHub Actions

If you have an existing workflow, add the following steps:

```yaml
...
steps:
    ...

    - name: Conventional Commitlint
      uses: opensource-nepal/commitlint@v1

    ...
```

If you don't have any workflows, create a new GitHub workflow file, e.g., `.github/workflows/commitlint.yaml`:

```yaml
name: Conventional Commitlint

on:
  push:
    branches: ['main']
  pull_request:

jobs:
  commitlint:
    runs-on: ubuntu-latest
    name: Conventional Commitlint
    steps:
      - name: Conventional Commitlint
        uses: opensource-nepal/commitlint@v1
```

> **_Note:_** The `commitlint` GitHub Action is triggered only by `push`, `pull_request`, or `pull_request_target` events.

#### GitHub Action Inputs

| #   | Name              | Type    | Default                | Description                                                           |
| --- | ----------------- | ------- | ---------------------- | --------------------------------------------------------------------- |
| 1   | **fail_on_error** | Boolean | `true`                 | Whether the GitHub Action should fail if commitlint detects an issue. |
| 2   | **verbose**       | Boolean | `false`                | Enables verbose output.                                               |
| 3   | **token**         | String  | `secrets.GITHUB_TOKEN` | GitHub Token for fetching commits using the GitHub API.               |

#### GitHub Action Outputs

| #   | Name          | Type    | Description                                                  |
| --- | ------------- | ------- | ------------------------------------------------------------ |
| 1   | **exit_code** | Integer | The exit code of the commitlint step.                        |
| 2   | **status**    | String  | The outcome of the commitlint step (`success` or `failure`). |

### Pre-commit

1. Add the following configuration to `.pre-commit-config.yaml`:

   ```yaml
   repos:
      ...
      - repo: https://github.com/opensource-nepal/commitlint
        rev: v1.3.0
        hooks:
          - id: commitlint
      ...
   ```

2. Install the `commit-msg` hook in your project repository:

   ```bash
   pre-commit install --hook-type commit-msg
   ```

   Running only `pre-commit install` will not work.

> **_Note:_** Avoid using commit messages that start with `#`, as this may cause unexpected behavior with `commitlint`.

## CLI (Command Line Interface)

For CLI usage, please refer to [cli.md](./docs/cli.md).

## Contribution

We appreciate feedback and contributions to this package. To get started, please see our [contribution guide](./CONTRIBUTING.md).
