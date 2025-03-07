from faker import Faker
from api.users_api import UsersApi

fake = Faker("en-US")


def new_user_data():
    """Генерация случайных данный пользователя"""

    return {"email": fake.ascii_email(), "password": fake.password(8), "name": "TestUser"}


def existing_user_data():
    """Генерация и регистрация нового пользователя"""

    user = new_user_data()
    response = UsersApi.register_user(user)
    assert response.success, "\nUser must be successfully registered "
    return user
