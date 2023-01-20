import json
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


USERNAME = 'test-username'
REPOSITORY = 'test-repository'


@pytest.fixture
def example_repository_data():
    return {
        'status_code': 200,
        'content': [{
            'name': REPOSITORY,
            "html_url": "https://some-url.com",
            "description": "test-description",
            "stargazers_count": 3
        }]
    }


@patch('backend.main.get_commit_count')
@patch('backend.main.get_repository_data')
def test_external_api_is_called(mock_repository, mock_commits, example_repository_data):
    mock_repository.return_value = example_repository_data
    client.get(f'/{USERNAME}/')
    mock_repository.assert_called_with(USERNAME)
    mock_commits.assert_called()


@patch('backend.main.get_repository_data')
def test_cannot_pass_too_long_username(mock):
    mock.return_value = {}  # It won't be called but still mocking just in case
    username = 'this-username-has-more-than-39-characters'
    response = client.get(f'/{username}/')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@patch('backend.main.get_commit_count')
@patch('backend.main.get_repository_data')
def test_return_data_contain_necessary_information(mock_repository, mock_commits, example_repository_data):
    commit_count = 2
    mock_repository.return_value = example_repository_data
    mock_commits.return_value = commit_count
    response = client.get(f'/{USERNAME}/')

    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert len(data) == len(example_repository_data['content'])
    # Check if values returned by request match data from external API
    assert all(item in data[0].values() for item in example_repository_data['content'][0].values())


@patch('backend.main.get_repository_data')
def test_appropriate_response_is_given_for_non_existing_user(mock):
    mock.return_value = {
        "status_code": 404,
        "content": {"message": "Not Found"}
    }
    response = client.get(f'/{USERNAME}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = json.loads(response.content)
    assert content['detail']['message'] == 'User not found, please try a different username.'


@patch('backend.main.get_repository_data')
@patch('backend.main.get_rate_reset_time')
def test_api_rate_limit_information_is_returned(mock_rate, mock_repository):
    mock_repository.return_value = {
        "status_code": 403,
        "content": {"message": "API rate limit exceeded for..."}
    }
    mock_rate.return_value = datetime.now() + timedelta(minutes=30)
    response = client.get(f'/{USERNAME}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = json.loads(response.content)
    assert content['detail']['message'].startswith('API rate limit exceeded, please try again in')
