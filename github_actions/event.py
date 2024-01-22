"""
This module defines the `GithubEvent` class for handling GitHub event details.

Note:
    This module relies on the presence of specific environment variables
    set by GitHub Actions.
"""
import json
import os
from typing import Any, Dict


# pylint: disable=R0902; Too many instance attributes
class GithubEvent:
    """Class representing GitHub events.

    This class provides methods for loading and accessing various details of
    GitHub events.

    Attributes:
        event_name (str): The name of the GitHub event.
        sha (str): The commit SHA associated with the event.
        ref (str): The Git reference (branch or tag) for the event.
        workflow (str): The name of the GitHub workflow.
        action (str): The action that triggered the event.
        actor (str): The GitHub username of the user or app that triggered the event.
        job (str): The name of the job associated with the event.
        run_attempt (str): The current attempt number for the job run.
        run_number (str): The unique number assigned to the run by GitHub.
        run_id (str): The unique identifier for the run.

        event_path (str): The path to the file containing the GitHub event payload.
        payload (dict): The GitHub event payload.

    Raises:
        EnvironmentError: If the required environment variable 'GITHUB_EVENT_PATH'
            is not found.

    Example:
        ```python
        github_event = GithubEvent()
        print(github_event.event_name)
        print(github_event.sha)
        print(github_event.payload)
        ```
    """

    def __init__(self) -> None:
        """Initialize a new instance of the GithubEvent class."""
        self.__load_details()

    def __load_details(self) -> None:
        """
        Load GitHub event details from environment variables and event payload file.

        This method initializes the instance attributes by reading values from
        environment variables set by GitHub Actions and loading the event payload
        from a file.
        """
        self.event_name = os.environ.get("GITHUB_EVENT_NAME")
        self.sha = os.environ.get("GITHUB_SHA")
        self.ref = os.environ.get("GITHUB_REF")
        self.workflow = os.environ.get("GITHUB_WORKFLOW")
        self.action = os.environ.get("GITHUB_ACTION")
        self.actor = os.environ.get("GITHUB_ACTOR")
        self.job = os.environ.get("GITHUB_JOB")
        self.run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
        self.run_number = os.environ.get("GITHUB_RUN_NUMBER")
        self.run_id = os.environ.get("GITHUB_RUN_ID")

        if "GITHUB_EVENT_PATH" not in os.environ:
            raise EnvironmentError("GITHUB_EVENT_PATH not found on the environment.")

        self.event_path = os.environ["GITHUB_EVENT_PATH"]
        with open(self.event_path, encoding="utf-8") as file:
            self.payload = json.load(file)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the GithubEvent instance to a dictionary.

        Returns:
            dict: A dictionary containing the attributes of the GithubEvent instance.
        """
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        }

    def __str__(self) -> str:
        """
        Returns string representation of the github event data.

        Returns:
            str: Github event data.
        """
        return str(self.to_dict())
