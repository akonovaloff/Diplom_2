import pytest
import allure
from api.stellar_burger_api import StellarBurgerApi
from conftest import new_user, existing_user


class TestUserRegistration:

    @classmethod
    def user_registration(cls, payload, expected_status, expected_message):
        """Проверяет ответ сервера на регистрацию пользователя с различным набором данных
        :param payload: словарь с параметрами пользователя
        :param expected_status: ожидаемый статус-код ответа сервера
        :param expected_message: ожидаемая подстрока, которая должна содержаться в ответе сервера
        :return:
        """
        response = StellarBurgerApi.register_user(payload)
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")

    @allure.title("Регистрация нового пользователя")
    def test_new_user_registration_new_user(self, new_user):
        self.user_registration(new_user, 200, '"success":true')

    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    @allure.title("Регистрация по неполным данным")
    def test_user_registration_existing_user_without_required_field(self, existing_user, field_to_remove):
        no_required_field_user = {key: value for key, value in existing_user.items() if key != field_to_remove}
        self.user_registration(no_required_field_user, 403, "Email, password and name are required fields")

    @allure.title("Регистрация пользователя, который уже существует")
    def test_user_registration_existing_user(self, existing_user):
        self.user_registration(existing_user, 403, "User already exists")
