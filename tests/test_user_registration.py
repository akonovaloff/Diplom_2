import pytest
from api.users_api import UsersApi
from utils.helpers import new_user_data

# Подготовка тестовых данных пользователей
new_user = new_user_data()
no_email_user = {key: value for key, value in new_user_data().items() if key != "email"}
no_pass_user = {key: value for key, value in new_user_data().items() if key != "password"}
no_name_user = {key: value for key, value in new_user_data().items() if key != "name"}


class TestUserRegistration:

    # Задаем параметры теста
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        # Unique user
        (new_user, 200, '"success":true'),
        # Missing required field (email)
        (no_email_user, 403, "Email, password and name are required fields"),
        # Missing required field (password)
        (no_pass_user, 403, "Email, password and name are required fields"),
        # Missing required field (name)
        (no_name_user, 403, "Email, password and name are required fields"),
    ])
    def test_user_registration(self, payload, expected_status, expected_message):
        """
        Тест проверяет ответ сервера на регистрацию пользователя с различным набором данных
        :param payload: словарь с параметрами пользователя
        :param expected_status: ожидаемый статус-код ответа сервера
        :param expected_message: ожидаемая подстрока, которая должна содержаться в ответе сервера
        :return:
        """
        print(f"\nРегистрация пользователя: {payload}")
        response = UsersApi.register_user(payload)
        print(f"Статус: {response.status_code} (ожидаемый: {expected_status})")
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")

    def test_registration_existing_user(self):
        """
        Тест проверяет невозможность зарегистрировать существующего пользователя
        :return:
        """
        payload = new_user_data()
        expected_status = 403
        expected_message = "User already exists"

        print(f"\nРегистрация пользователя: {payload}")
        response = UsersApi.register_user(payload)
        assert response.status_code == 200, "\nКод ответа сервера не соответствует ожидаемому"

        print(f"Регистрация существующего пользователя: {payload}")
        response = UsersApi.register_user(payload)

        print(f"Статус: {response.status_code} (ожидаемый: {expected_status})")
        assert response.status_code == expected_status, "\nКод ответа сервера не соответствует ожидаемому"
        assert expected_message in response.text, (
            f"\nТекст ответа сервера не содержит ожидаемую часть '{expected_message}'"
            f"\nОтвет сервера: {response.text}")
        print("Ok")
