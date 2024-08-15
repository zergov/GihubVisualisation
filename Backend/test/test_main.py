import json
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture
def expected_json_data():
    with open('test/resources/expected_commits.json') as f:
        data = json.load(f)
    return data


def test_read_main(expected_json_data):
    params = {
        "repo_path": "https://github.com/cedric-audy/test_repo_pfe",
        "days": 3000
    }
    response = client.get("/commits/", params=params)
    assert response.status_code == 200
    assert response.json() == expected_json_data
