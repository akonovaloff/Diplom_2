from faker import Faker
from api.stellar_burger_api import StellarBurgerApi as Api


class StellarBurgerUser:
    fake = Faker("en-US")
    api = Api

    def __init__(self):

        self.email: str = ""
        self.password: str = ""
        self.name = "TestUser"

        self.generate_email()
        self.generate_password()

        self.__server_email: str = self.email
        self.__server_name: str = self.name
        self.__server_password: str = self.password
        self.__is_registered = False
        self.__access_token: str = ""
        self.__refresh_token: str = ""

        self._payload = self.Payload(self)  # Инициализируем вложенный класс
        print(self)

    def __del__(self):
        if self.__is_registered:
            response = self.api.delete_user(self.__access_token)

    def __repr__(self):
        return f"StellarBurgerUser: {self.payload.full}"

    def generate_email(self):
        self.email = self.fake.ascii_email()

    def generate_password(self):
        self.password = self.fake.password(8)

    def generate_name(self):
        self.name = self.fake.first_name()

    @property
    def payload(self):
        # Возвращаем экземпляр Payload, чтобы можно было обращаться к no_password, no_email и т.д.
        return self._payload

    class Payload:
        def __init__(self, user):
            self.user = user

        @property
        def full(self):
            # Возвращает полный словарь
            return {
                "email": self.user.email,
                "password": self.user.password,
                "name": self.user.name
            }

        @property
        def no_password(self):
            # Возвращает словарь без password
            return {
                "email": self.user.email,
                "name": self.user.name
            }

        @property
        def no_name(self):
            # Возвращает словарь без name
            return {
                "email": self.user.email,
                "password": self.user.password
            }

        @property
        def no_email(self):
            # Возвращает словарь без email
            return {
                "password": self.user.password,
                "name": self.user.name
            }

    def registration(self):
        response = self.api.register_user(self.payload.full)
        if response.success:
            self.__is_registered = True
            self.__access_token = response.data['accessToken']
            self.__refresh_token = response.data['refreshToken']
            self.__update_server_info()
        return response

    def update_info(self):
        response = self.api.patch_user_info(self.__access_token, self.payload.full)
        if response.success:
            self.__update_server_info()
        else:
            self.__restore_server_info()
        return response

    def __update_server_info(self):
        is_info_updated = False
        if self.__server_name != self.name:
            is_info_updated = True
            self.__server_name = self.name
        if self.__server_password != self.password:
            is_info_updated = True
            self.__server_password = self.password
        if self.__server_email != self.email:
            is_info_updated = True
            self.__server_email = self.email
        if is_info_updated:
            print(self)

    def __restore_server_info(self):
        self.name = self.__server_name
        self.password = self.__server_password
        self.email = self.__server_email

    def login(self):
        response = self.api.login_user(self.payload.no_name)
        if response.success:
            self.__update_server_info()
            self.__access_token = response.data['accessToken']
            self.__refresh_token = response.data['refreshToken']
        else:
            self.__restore_server_info()
        return response

    def logout(self):
        response = self.api.logout_user(refresh_token=self.__refresh_token)
        return response
