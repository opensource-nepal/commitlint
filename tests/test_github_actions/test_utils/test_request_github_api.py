# type: ignore
# pylint: disable=all
import json
from unittest.mock import Mock, patch

import pytest

from github_actions.action.utils import request_github_api


@pytest.fixture
def mock_https_connection():
    with patch("http.client.HTTPSConnection") as mock:
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode("utf-8")
        mock_response.status = 200
        mock.return_value.getresponse.return_value = mock_response

        yield mock


def test__request_github_api__get_request(mock_https_connection):
    status, data = request_github_api(
        method="GET", url="/repos/opensource-nepal/commitlint", token="test_token"
    )

    assert status == 200
    assert data == {"success": True}

    mock_https_connection.return_value.request.assert_called_with(
        method="GET",
        url="/repos/opensource-nepal/commitlint",
        body=None,
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )


def test__request_github_api__get_request_with_params(mock_https_connection):
    status, data = request_github_api(
        method="GET",
        url="/repos/opensource-nepal/commitlint",
        token="test_token",
        params={"key1": "val1", "key2": "val2"},
    )

    assert status == 200
    assert data == {"success": True}

    mock_https_connection.return_value.request.assert_called_with(
        method="GET",
        url="/repos/opensource-nepal/commitlint?key1=val1&key2=val2",
        body=None,
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )


def test__request_github_api__post_request(mock_https_connection):
    status, data = request_github_api(
        method="POST",
        url="/repos/opensource-nepal/commitlint",
        token="test_token",
    )

    assert status == 200
    assert data == {"success": True}

    mock_https_connection.return_value.request.assert_called_with(
        method="POST",
        url="/repos/opensource-nepal/commitlint",
        body=None,
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )


def test_request_github_api__post_request_with_body(mock_https_connection):
    status, data = request_github_api(
        method="POST",
        url="/repos/opensource-nepal/commitlint",
        token="test_token",
        body={"data": "test_data"},
    )

    assert status == 200
    assert data == {"success": True}

    mock_https_connection.return_value.request.assert_called_with(
        method="POST",
        url="/repos/opensource-nepal/commitlint",
        body=json.dumps({"data": "test_data"}),
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )


def test_request_github_api__post_request_with_body_and_params(mock_https_connection):
    status, data = request_github_api(
        method="POST",
        url="/repos/opensource-nepal/commitlint",
        token="test_token",
        body={"data": "test_data"},
        params={"key1": "val1", "key2": "val2"},
    )

    assert status == 200
    assert data == {"success": True}

    mock_https_connection.return_value.request.assert_called_with(
        method="POST",
        url="/repos/opensource-nepal/commitlint?key1=val1&key2=val2",
        body=json.dumps({"data": "test_data"}),
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "User-Agent": "commitlint",
        },
    )
