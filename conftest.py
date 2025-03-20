import pytest
from faker import Faker
from api.stellar_burger_api import StellarBurgerApi
from utils.helpers import StellarBurgerUser

fake = Faker("en-US")


@pytest.fixture
def new_user():
    """Генерация случайных данных пользователя"""

    user = {"email": fake.ascii_email(), "password": fake.password(8), "name": "TestUser"}
    print("Данные пользователя сгенерированы")
    yield user

    response = StellarBurgerApi.login_user(user)
    if response.success:
        _ = StellarBurgerApi.delete_user(response.data["accessToken"])
        print("Пользователь удалён")
    else:
        print("Пользователь отсутствует в базе")


@pytest.fixture
def existing_user(new_user):
    """Генерация и регистрация нового пользователя"""

    user = new_user
    response = StellarBurgerApi.register_user(user)
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


@pytest.fixture()
def new_stellar_burger_user():
    print("Создание пользователя")
    user = StellarBurgerUser()
    print("Регистрация пользователя")
    user.registration()
    return user


@pytest.fixture()
def logout_stellar_burger_user(new_stellar_burger_user):
    print("Выход из системы")
    new_stellar_burger_user.logout()
    return new_stellar_burger_user


@pytest.fixture()
def login_stellar_burger_user(new_stellar_burger_user):
    print("Вход в систему")
    new_stellar_burger_user.login()
    return new_stellar_burger_user


@pytest.fixture(scope="session")
def ingredients():
    return StellarBurgerApi.get_available_ingredients().data["data"]
