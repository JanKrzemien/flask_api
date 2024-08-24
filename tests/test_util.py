import pytest
from flask import jsonify
import src.flaskr.util as util
from tests.common_fixtures import app

@pytest.fixture
def json_completed_request_response_data(app):
    return jsonify({
        "status_code": 200
    })

def test_json_completed_request(json_completed_request_response_data, app):
    assert util.json_request_completed().response[0] == json_completed_request_response_data.response[0]

@pytest.fixture
def json_error_response_data(app):
    return jsonify({
        "error": "er",
        "status_code": 400
    })

def test_json_error(json_error_response_data, app):
    assert util.json_error("er", 400).response[0] == json_error_response_data.response[0]

@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("True",1),
        ("False",0),
        ("asda",0),
        (None,0),
        (1,0),
    ]
)
def test_get_admin_int_value(test_input, expected):
    assert util.get_admin_int_value(test_input) == expected