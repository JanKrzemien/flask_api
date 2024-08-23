import pytest
import json
from ..flaskr.util import json_request_completed

@pytest.fixture
def json_completed_request_response_data():
    try:
        return json.dumps({
            "status_code": 200
        })
    except TypeError:
        pass

def test_completed_request(json_completed_request_response_data):
    assert json_request_completed() == json_completed_request_response_data