import pytest
import allure
from api.stellar_burger_api import StellarBurgerApi
from conftest import new_user, existing_user


class TestUserRegistration:

    @allure.title("Регистрация нового пользователя")
    def test_new_user_registration_new_user(self, new_user):
        expected_message = '"success":true'
        response = StellarBurgerApi.register_user(new_user)
        assert response.status_code == 200, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")

    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    @allure.title("Регистрация по неполным данным")
    def test_user_registration_existing_user_without_required_field(self, existing_user, field_to_remove):
        no_required_field_user = {key: value for key, value in existing_user.items() if key != field_to_remove}
        expected_message = "Email, password and name are required fields"
        response = StellarBurgerApi.register_user(no_required_field_user)
        assert response.status_code == 403, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")

    @allure.title("Регистрация пользователя, который уже существует")
    def test_user_registration_existing_user(self, existing_user):
        expected_message = "User already exists"
        response = StellarBurgerApi.register_user(existing_user)
        assert response.status_code == 403, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
