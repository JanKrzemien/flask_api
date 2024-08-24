import pytest
import src.flaskr.__init__ as init

class TestConfig:
    TESTING=True
    SECRET_KEY='test'
    TOKEN_EXPIRATION=180
    ACCESS_TOKEN_TYPE='access_token'
    REFRESH_TOKEN_TYPE='refresh_token'

@pytest.fixture
def app():
    flask_app = init.create_app(test_config=TestConfig())
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client