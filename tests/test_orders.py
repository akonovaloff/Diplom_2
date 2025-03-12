import pytest
import requests
import allure
from random import choices, randint

from utils.config import ApiEndpoints
from utils.helpers import StellarBurgerUser
from api.stellar_burger_api import StellarBurgerApi as Api


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestOrders:
    def setup_class(self):
        """Подготовительный шаг перед тестами"""
        with allure.step("Регистрация для авторизованного пользователя"):
            self.user = StellarBurgerUser()
            response = self.user.registration()
            assert response.success is True
            self.authorized_header = {"Authorization": self.user.access_token}

        with allure.step("Регистрация и выход для неавторизованного пользователя"):
            self.unauthorized_user = StellarBurgerUser()
            response = self.unauthorized_user.registration()
            assert response.success is True
            self.unauthorized_user.logout()
            self.unauthorized_header = {"Authorization": self.unauthorized_user.access_token}

        with allure.step("Подготовка токенов авторизации и данных заказа"):
            self.empty_header = {}

            available_ingredients_list = Api.get_available_ingredients().data["data"]
            ingredients_id_list = choices(available_ingredients_list, k=randint(1, 5))
            self.valid_ingredients_payload = {"ingredients": [ingredient["_id"] for ingredient in ingredients_id_list]}
            self.invalid_ingredients_payload = {"ingredients": [""]}
            self.empty_payload = {}

    @allure.story("Создание заказа с разными условиями")
    @pytest.mark.parametrize("headers_attr, payload_attr, expected_code", [
        ("authorized_header", "valid_ingredients_payload", 200),  # Валидный токен + валидные ингредиенты
        ("authorized_header", "invalid_ingredients_payload", 500),  # Валидный токен + невалидные ингредиенты
        ("authorized_header", "empty_payload", 400),  # Валидный токен + пустой payload
        ("unauthorized_header", "valid_ingredients_payload", 401),  # Невалидный токен + валидные ингредиенты
    ])
    def test_create_order(self, headers_attr, payload_attr, expected_code):
        """
        Параметризованный тест для создания заказа.
        Данные подготавливаются в setup_method.
        """
        with allure.step(f"Получение данных: {headers_attr}, {payload_attr}"):
            headers = getattr(self, headers_attr)
            payload = getattr(self, payload_attr)

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(url=ApiEndpoints.orders, headers=headers, json=payload)
            response = Api.HandledResponse(response, expected_code)
        with allure.step(f"Проверка статус-кода (ожидаемый {expected_code})"):
            assert response.status_code == expected_code, f"Ожидался код {expected_code}, но получен {response.status_code}"

    def teardown_class(self):
        """
        Явный вызов удаления созданных пользователей
        """
        with allure.step("Удаление созданных пользователей"):
            self.user.__del__()
            self.unauthorized_user.__del__()