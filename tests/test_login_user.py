import pytest
from api.stellar_burger_api import StellarBurgerApi
from conftest import new_user, existing_user, not_valid_pass_user, no_password_user
import allure


class TestLoginUser:

    @allure.title("Вход не зарегистрированного пользователя")
    def test_login_user_new_user(self, new_user):
        """Логин нового не зарегистрированного пользователя"""
        response = StellarBurgerApi.login_user(new_user)
        assert response.status_code == 401, "\nКод ответа сервера не соответствует ожидаемому"
        assert "email or password are incorrect" in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть 'email or password are incorrect'"
            f"\nОтвет сервера: {response.text}")

    @allure.title("Вход зарегистрированного пользователя")
    def test_login_user_existing_user(self, existing_user):
        """Логин существующего пользователя"""
        response = StellarBurgerApi.login_user(existing_user)
        assert response.status_code == 200, "\nКод ответа сервера не соответствует ожидаемому"
        assert '"success":true' in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть 'email or password are incorrect'"
            f"\nОтвет сервера: {response.text}")

    @allure.title("Попытка входа с неправильным паролем")
    def test_login_user_existing_user_but_incorrect_password(self, not_valid_pass_user):
        """Логин существующего пользователя с некорректным паролем"""
        response = StellarBurgerApi.login_user(not_valid_pass_user)
        assert response.status_code == 401, "\nКод ответа сервера не соответствует ожидаемому"
        assert "email or password are incorrect" in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть 'email or password are incorrect'"
            f"\nОтвет сервера: {response.text}")

    @allure.title("Вход пользователя без поля 'пароль' в запросе")
    def test_login_user_existing_user_but_no_password_field(self, no_password_user):
        """Логин существующего пользователя без поля "пароль" в запросе"""
        response = StellarBurgerApi.login_user(no_password_user)
        assert response.status_code == 401, "\nКод ответа сервера не соответствует ожидаемому"
        assert "email or password are incorrect" in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть 'email or password are incorrect'"
            f"\nОтвет сервера: {response.text}")
