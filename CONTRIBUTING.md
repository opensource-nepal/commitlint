# Contributing Guide

Thank you for your interest in contributing to the **commitlint** project!
Your contributions will help improve and enhance this tool.
Please take a moment to review the following guidelines before getting started.

## Prerequisites

Before contributing, ensure that you have the following:

- **Python 3.10 or higher** installed. Download it from the [official Python website](https://www.python.org/downloads/).
- **Poetry** installed for dependency management. Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation).

## Getting Started

To set up the project on your local machine, follow these steps:

1. **Fork** the repository on GitHub.
2. **Clone** the forked repository to your local machine:

   ```bash
   git clone https://github.com/<your-username>/commitlint.git
   cd commitlint
   ```

3. **Install dependencies**:

   ```bash
   poetry install
   ```

4. **Verify your setup**:

   ```bash
   poetry run commitlint --version
   ```

## Tests

Run tests

```bash
poetry run pytest
```

Run tests with coverage

```bash
poetry run pytest --cov=src
```

Generate html coverage

```bash
poetry run pytest --cov=src/ --cov-report=html
```

## Use pre-commit hook

Install pre-commit hook using the command below.

```bash
poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Pull Requests

We welcome and appreciate pull requests from the community. To contribute:

1. **Fork** the repository and create a new branch based on the `main` branch:

   ```bash
   git checkout -b <your-branch-name>
   ```

2. **Write tests** for your changes if applicable.
3. **Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)** for commit messages.
   Examples:

   - `feat: add commit message validation`
   - `fix(parser): resolve message parsing issue`

4. **Push** your branch to your forked repository:

   ```bash
   git push origin <your-branch-name>
   ```

5. **Create a Pull Request**:

   - Open a pull request from your branch to the `main` branch of the original repository.
   - Provide a clear and concise description of the changes, along with relevant context.

6. **Review & Feedback**:

   - Participate in the code review process and address any feedback promptly.

## License

By contributing to this project, you agree that your contributions will be licensed under the **GPL-3.0 License**.
Refer to the [LICENSE](./LICENSE) file for more details.

## Other Ways to Contribute

Even if you don’t contribute code, you can still help:

- **Spread the word** about this tool.
- Write a blog or article about how you use this project.
- Share your best practices, examples, or ideas with us.

Thank you for contributing to **commitlint**! 🎉
