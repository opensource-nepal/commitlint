# How to Contribute

## Install Development Dependencies (Using Pipenv)

All the dependencies are managed by Pipenv. Please install Pipenv on your system first by following the instructions at [https://pipenv.pypa.io/en/latest/installation.html](https://pipenv.pypa.io/en/latest/installation.html).

Once Pipenv is installed, you can install the development dependencies by running the following command:

```bash
pipenv install --dev
```

## Install pre-commit hooks

To install pre-commit and commit-msg hook for this project, run the following command:

```bash
pipenv run install-hooks
```

## Run tests

Run the tests using the below command:

```bash
pipenv run test
```

## Before submitting

Before submitting your Pull Request, please do the following steps:

1. Add any changes you want.
1. Add tests for the new changes.
1. Edit documentation (`README.md`) if you have changed something significant.
1. Commit your changes using [semantic commit message](https://seesparkbox.com/foundry/semantic_commit_messages).
   Examples: `"fix: Fixed foobar bug"`, `"feat(accounts): Added foobar feature on accounts"`.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write a short article on how you are using this project.
You can also share your best practices with us.
