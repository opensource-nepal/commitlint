"""Utility functions for GitHub Actions"""

import http.client
import json
import os
import urllib.parse
from typing import Any, Dict, Optional, Tuple, Union


def get_input(key: str) -> str:
    """
    Read the GitHub action input.

    Args:
        key (str): Input key.

    Returns:
        str: The value of the input.
    """
    key = key.upper()
    return os.environ[f"INPUT_{key}"]


def get_boolean_input(key: str) -> bool:
    """
    Parse the input environment key of boolean type in the YAML 1.2
    "core schema" specification.
    Support boolean input list:
    `true | True | TRUE | false | False | FALSE`.
    ref: https://yaml.org/spec/1.2/spec.html#id2804923

    Args:
        key (str): Input key.

    Returns:
        bool: The parsed boolean value.

    Raises:
        TypeError: If the environment variable's value does not meet the
        YAML 1.2 "core schema" specification for booleans.
    """
    val = get_input(key)

    if val.upper() == "TRUE":
        return True

    if val.upper() == "FALSE":
        return False

    raise TypeError(
        """
        Input does not meet YAML 1.2 "Core Schema" specification.\n'
        Support boolean input list:
        `true | True | TRUE | false | False | FALSE`.
        """
    )


def write_line_to_file(filepath: str, line: str) -> None:
    """
    Write line to a specified filepath.

    Args:
        filepath (str): The path of the file.
        line (str): The Line to write in the file.
    """
    with open(file=filepath, mode="a", encoding="utf-8") as output_file:
        output_file.write(f"{line}\n")


def write_output(name: str, value: Union[str, int]) -> None:
    """
    Write an output to the GitHub Actions environment.

    Args:
        name (str): The name of the output variable.
        value (Union[str, int]): The value to be assigned to the output variable.
    """
    output_filepath = os.environ["GITHUB_OUTPUT"]
    write_line_to_file(output_filepath, f"{name}={value}")


def request_github_api(
    method: str,
    url: str,
    token: str,
    body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Tuple[int, Any]:
    """
    Sends a request to the GitHub API.

    Args:
        method (str): The HTTP request method, e.g., "GET" or "POST".
        url (str): The endpoint URL for the GitHub API.
        token (str): The GitHub API token for authentication.
        body (Optional[Dict[str, Any]]): The request body as a dictionary.
        params (Optional[Dict[str, str]]): The query parameters as a dictionary.

    Returns:
        Tuple[int, Any]: A tuple with the status as the first element and the response
            data as the second element.

    """
    if params:
        url += "?" + urllib.parse.urlencode(params)

    conn = http.client.HTTPSConnection(host="api.github.com")
    conn.request(
        method=method,
        url=url,
        body=json.dumps(body) if body else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )
    res = conn.getresponse()
    json_data = res.read().decode("utf-8")
    data = json.loads(json_data)

    return res.status, data
