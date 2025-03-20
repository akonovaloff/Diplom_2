import pytest
from api.stellar_burger_api import StellarBurgerApi
from conftest import new_user, existing_user, not_valid_pass_user, no_password_user
import allure

class TestLoginUser:

    @classmethod
    def login_user(cls, payload, expected_status, expected_message):
        """Отправляет запрос на вход с разными данными пользователя и проверяет ответ сервера
        """
        response = StellarBurgerApi.login_user(payload)
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")

    @allure.title("Вход не зарегистрированного пользователя")
    def test_login_user_new_user(self, new_user):
        """Логин нового не зарегистрированного пользователя"""
        self.login_user(new_user, 401, "email or password are incorrect")

    @allure.title("Вход зарегистрированного пользователя")
    def test_login_user_existing_user(self, existing_user):
        """Логин существующего пользователя"""
        self.login_user(existing_user, 200, '"success":true')

    @allure.title("Попытка входа с неправильным паролем")
    def test_login_user_existing_user_but_incorrect_password(self, not_valid_pass_user):
        """Логин существующего пользователя с некорректным паролем"""
        self.login_user(not_valid_pass_user, 401, "email or password are incorrect")

    @allure.title("Вход пользователя без поля 'пароль' в запросе")
    def test_login_user_existing_user_but_no_password_field(self, no_password_user):
        """Логин существующего пользователя без поля "пароль" в запросе"""
        self.login_user(no_password_user, 401, "email or password are incorrect")
