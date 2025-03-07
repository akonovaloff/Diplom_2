import pytest
from utils.config import ApiEndpoints
from api.users_api import UsersApi
from utils.helpers import existing_user_data

BASE_URL = ApiEndpoints.login

existing_user = existing_user_data()

class TestLoginExistingUser:
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        (existing_user, 200, '"success":true')
    ])
    def test_login_existing_user(self, payload, expected_status, expected_message):
        response = UsersApi.login_user(payload)
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")
