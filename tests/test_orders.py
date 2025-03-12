import pytest
import requests
import allure
from random import choices, randint

from utils.config import ApiEndpoints
from utils.helpers import StellarBurgerUser
from api.stellar_burger_api import StellarBurgerApi as Api


class TestOrders:
    def setup_method(self):
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

        with allure.step("Подготовка пользователя с не пустой историей заказов"):
            user_with_orders = StellarBurgerUser()
            user_with_orders.registration()
            requests.post(url=ApiEndpoints.orders,
                                     headers={"Authorization": user_with_orders.access_token},
                                     json={"ingredients": [ingredient["_id"] for ingredient in ingredients_id_list]})
            self.user_with_orders = {"Authorization": user_with_orders.access_token}

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
            assert response.status_code == expected_code, (
                f"Ожидался код {expected_code}, но получен {response.status_code}: ({headers_attr}, {payload_attr})\n"
                f"Запрос:\n"
                f"\turl= {response.response.request.url}\n"
                f"\theaders={response.response.request.headers}\n"
                f"\tpayload={response.response.request.body}\n\n"
                f"Ответ сервера:\n"
                f"\ttext={response.response.text}\n")

    @pytest.mark.parametrize("headers_attr, expected_code, expected_orders_len", [
        ("authorized_header", 200, 0),  # Валидный токен
        ("unauthorized_header", 200, 0),  # Невалидный токен
        ("user_with_orders", 200, 1)
    ])
    def test_get_user_orders(self, headers_attr, expected_code, expected_orders_len):
        """
        Параметризованный тест для проверки созданных заказов пользователя.
        Данные подготавливаются в setup_method.
        """
        # Получаем данные для теста
        headers = getattr(self, headers_attr)
        # Отправляем запрос
        response = Api.get_orders(headers=headers)
        # Проверяем статус-код
        assert response.status_code == expected_code, (
            f"Ожидался код {expected_code}, но получен {response.status_code}")
        # Проверяем, что число заказов соответствует ожидаемому
        assert len(response.data['orders']) == expected_orders_len, "Ответ сервера должен содержать ожидаемое число заказов"

        # Если массив заказов не пустой, то проверяем наличие обязательных полей
        if expected_orders_len != 0:
            for order in response.data['orders']:
                for field in ['_id', 'ingredients', 'status', 'name', 'createdAt', 'updatedAt', 'number']:
                    assert field in order.keys(), "Заказ должен содержать все обязательные поля"

    def teardown_method(self):
        """
        Явный вызов удаления созданных пользователей
        """
        with allure.step("Удаление созданных пользователей"):
            self.user.__del__()
            self.unauthorized_user.__del__()
