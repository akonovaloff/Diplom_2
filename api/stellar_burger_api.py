import requests
from utils.config import ApiEndpoints
import inspect


class StellarBurgerApi:
    class HandledResponse:
        def __init__(self, response: requests.Response, success_code: int, show_response: bool = True):
            self.response = response
            self.success = response.status_code == success_code
            self.status_code = response.status_code
            self.text = response.text
            self.__caller = inspect.currentframe().f_back.f_back.f_code.co_name
            try:
                self.data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.data = {}

            if show_response:
                print(self)

        def __repr__(self):
            return f"{self.__caller}:(success={self.success}, status_code={self.status_code}, data={self.data})"

    @classmethod
    def register_user(cls, payload: dict) -> HandledResponse:
        """Отправляет POST-запрос на регистрацию пользователя"""

        response = requests.post(ApiEndpoints.register, json=payload)

        return cls.HandledResponse(response, 200)

    @classmethod
    def delete_user(cls, access_token: str) -> HandledResponse:
        """Отправляет DELETE-запрос на удаление пользователя по его accessToken"""

        headers = {"Authorization": access_token}
        response = requests.delete(ApiEndpoints.user, headers=headers)

        return cls.HandledResponse(response, 202)

    @classmethod
    def login_user(cls, payload: dict) -> HandledResponse:
        """Отправляет POST-запрос, чтобы залогинить пользователя в системе"""

        response = requests.post(ApiEndpoints.login, json=payload)

        return cls.HandledResponse(response, 200)

    @classmethod
    def logout_user(cls, refresh_token: str) -> HandledResponse:
        payload = {"token": refresh_token}
        response = requests.post(ApiEndpoints.logout, json=payload)
        return cls.HandledResponse(response, 200)

    @classmethod
    def get_user_info(cls, access_token: str):
        headers = {"Authorization": access_token}
        response = requests.get(ApiEndpoints.user, headers=headers)
        return cls.HandledResponse(response, 200)

    @classmethod
    def patch_user_info(cls, access_token: str, payload: dict) -> HandledResponse:
        headers = {"Authorization": access_token}
        response = requests.patch(ApiEndpoints.user, headers=headers, json=payload)
        return cls.HandledResponse(response, 200)

    @classmethod
    def get_available_ingredients(cls) -> HandledResponse:
        response = requests.get(ApiEndpoints.ingredients)
        return cls.HandledResponse(response, 200, False)

    @classmethod
    def post_orders(cls, headers: dict, payload: dict) -> HandledResponse:
        response = requests.post(ApiEndpoints.orders, headers=headers, json=payload)
        return cls.HandledResponse(response, 200)

    @classmethod
    def get_orders(cls, headers: dict) -> HandledResponse:
        response = requests.get(ApiEndpoints.orders, headers=headers)
        return cls.HandledResponse(response, 200)