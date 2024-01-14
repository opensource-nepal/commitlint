# commitlint

commitlint is is a pre-commit hook designed to lint your commit messages according to the [Conventional Commits](https://www.conventionalcommits.org/) standard.

## How to use

1. Add the following configuration on `.pre-commit-config.yaml`.

    ```yaml
    repos:
    ...

    - repo: https://github.com/opensource-nepal/commitlint
        rev: 0.1.0
        hooks:
        - id: commitlint

    ...
    ```

2. Install the `commit-msg` hook in your project repo:

    ```bash
    pre-commit install --hook-type commit-msg
    ```

> **_NOTE:_**  Installing just using `pre-commit install` will not work.

## Contribution

We appreciate feedback and contribution to this package. To get started please see our [contribution guide](./CONTRIBUTING.md).
