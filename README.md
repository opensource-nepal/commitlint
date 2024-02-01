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

## Contribution

We appreciate feedback and contribution to this package. To get started please see our [contribution guide](./CONTRIBUTING.md).
