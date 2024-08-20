# type: ignore
# pylint: disable=all
import os


def set_github_env_vars():
    # GitHub Action event env
    os.environ["GITHUB_EVENT_NAME"] = "push"
    os.environ["GITHUB_SHA"] = "commitlint_sha"
    os.environ["GITHUB_REF"] = "refs/heads/main"
    os.environ["GITHUB_WORKFLOW"] = "commitlint_ci"
    os.environ["GITHUB_ACTION"] = "action"
    os.environ["GITHUB_ACTOR"] = "actor"
    os.environ["GITHUB_REPOSITORY"] = "opensource-nepal/commitlint"
    os.environ["GITHUB_JOB"] = "job"
    os.environ["GITHUB_RUN_ATTEMPT"] = "9"
    os.environ["GITHUB_RUN_NUMBER"] = "8"
    os.environ["GITHUB_RUN_ID"] = "7"
    os.environ["GITHUB_EVENT_PATH"] = "/tmp/github_event.json"
    os.environ["GITHUB_STEP_SUMMARY"] = "/tmp/github_step_summary"
    os.environ["GITHUB_OUTPUT"] = "/tmp/github_output"

    # GitHub Action input env
    os.environ["INPUT_TOKEN"] = "token"
    os.environ["INPUT_VERBOSE"] = "false"
    os.environ["INPUT_FAIL_ON_ERROR"] = "true"
