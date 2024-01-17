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
