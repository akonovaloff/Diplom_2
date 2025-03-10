import pytest
from faker import Faker
from api.users_api import UsersApi

fake = Faker("en-US")


@pytest.fixture
def new_user():
    """Генерация случайных данных пользователя"""

    user = {"email": fake.ascii_email(), "password": fake.password(8), "name": "TestUser"}
    print("Данные пользователя сгенерированы")
    yield user

    response = UsersApi.login_user(user)
    if response.success:
        _ = UsersApi.delete_user(response.data["accessToken"])
        print("Пользователь удалён")
    else:
        print("Пользователь отсутствует в базе")


@pytest.fixture
def existing_user(new_user):
    """Генерация и регистрация нового пользователя"""

    user = new_user
    response = UsersApi.register_user(user)
    assert response.success, "\nUser must be successfully registered "
    print("Пользователь зарегистрирован")
    return user


@pytest.fixture
def not_valid_pass_user(existing_user):
    user = {key: value for key, value in existing_user.items() if key != "password"}
    user["password"] = fake.password()
    return user

@pytest.fixture
def no_password_user(existing_user):
    user = {key: value for key, value in existing_user.items() if key != "password"}
    return user
#
# @pytest.fixture()
# def not_valid_email_user_data(existing_user_data):
#     user = {key: value for key, value in existing_user_data.items() if key != "email"}
#     user["email"] = fake.ascii_email()
#     return user
