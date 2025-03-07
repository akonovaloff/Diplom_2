import requests
from utils.config import ApiEndpoints
import inspect

class HandledResponse:
    def __init__(self, response: requests.Response, success_code: int):
        self.success = response.status_code == success_code
        self.status_code = response.status_code
        self.data = response.json()
        self.text = response.text
        print(self)

    def __repr__(self):
        return f"\n{inspect.currentframe().f_back.f_back.f_code.co_name}:(success={self.success}, status_code={self.status_code}, data={self.data})"


class UsersApi:
    @staticmethod
    def register_user(payload: dict) -> HandledResponse:
        """Отправляет POST-запрос на регистрацию пользователя"""

        response = requests.post(ApiEndpoints.register, json=payload)

        return HandledResponse(response, 200)

    @staticmethod
    def delete_user(token: str) -> HandledResponse:
        """Отправляет DELETE-запрос на удаление залогиненного пользователя"""

        response = requests.delete(ApiEndpoints.user)

        return HandledResponse(response, 200)

    @staticmethod
    def login_user(payload: dict) -> HandledResponse:
        """Отправляет POST-запрос, чтобы залогинить пользователя в системе"""

        response = requests.post(ApiEndpoints.login, json=payload)

        return HandledResponse(response, 200)
