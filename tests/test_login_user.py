import pytest
from api.users_api import UsersApi
from conftest import new_user, existing_user, not_valid_pass_user, no_password_user


class TestLoginUser:

    @classmethod
    def login_user(cls, payload, expected_status, expected_message):
        """Отправляет запрос на вход с разными данными пользователя и проверяет ответ сервера
        """
        response = UsersApi.login_user(payload)
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")

    def test_login_new_user(self, new_user):
        """Логин нового не зарегистрированного пользователя"""
        self.login_user(new_user, 401, "email or password are incorrect")

    def test_login_existing_user(self, existing_user):
        """Логин существующего пользователя"""
        self.login_user(existing_user, 200, '"success":true')

    def test_login_existing_user_by_incorrect_password(self, not_valid_pass_user):
        """Логин существующего пользователя с некорректным паролем"""
        self.login_user(not_valid_pass_user, 401, "email or password are incorrect")

    def test_login_no_password_user(self, no_password_user):
        """Логин существующего пользователя без поля "пароль" в запросе"""
        self.login_user(no_password_user, 401, "email or password are incorrect")
