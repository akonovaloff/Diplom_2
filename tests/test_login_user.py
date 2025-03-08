import pytest
from api.users_api import UsersApi
from utils.helpers import existing_user_data, new_user_data

# Подготовка тестовых данных
existing_user = existing_user_data()
new_user = new_user_data()
not_valid_pass = {"email": existing_user["email"], "password": new_user["password"]}
no_pass_user = {key: value for key, value in new_user.items() if key != "password"}


class TestLoginExistingUser:
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        # Существующий пользователь
        (existing_user, 200, '"success":true'),
        # Новый пользователь
        (new_user, 401, "email or password are incorrect"),
        # Валидный email, не валидный пароль
        (not_valid_pass, 401, "email or password are incorrect"),
        # Отсутствует поле password
        (no_pass_user, 401, "email or password are incorrect")
    ])
    def test_login_existing_user(self, payload, expected_status, expected_message):
        response = UsersApi.login_user(payload)
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")
