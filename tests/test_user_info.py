import pytest
import allure
from conftest import new_stellar_burger_user, login_stellar_burger_user


class TestUserInfo:
    @pytest.mark.parametrize("fields", [["email"], ["name"], ["email", "name"]])
    @allure.title("Изменение данных пользователя")
    def test_patch_user_info_name_or_email(self, login_stellar_burger_user, fields):
        """Тест проверяет возможность изменить email и name для залогиненного пользователя"""

        user = login_stellar_burger_user
        available_attr = ["email", "name"]
        old = {}
        for field in fields:
            assert field in available_attr, f"Недопустимое имя аттрибута: {field}. Допустимые аттрибуты: {available_attr}"
            old[field] = getattr(user, field)
            method_name = f"generate_{field}"
            generate_method = getattr(user, method_name)
            generate_method()
        response = user.update_info()
        for field in fields:
            assert response.data['user'][field] != old[field], f"Значение аттрибута {field} должно успешно измениться"

    @allure.title("Изменение пароля")
    def test_patch_user_password(self, login_stellar_burger_user):
        """Тест проверяет возможность изменить password для залогиненного пользователя.
        Поскольку сервер не возвращает пароль пользователя в явном виде, то проверка осуществляется
        через возможность залогиниться с новым паролем"""

        user = login_stellar_burger_user
        old_password = user.password
        user.generate_password()
        assert user.password != old_password, "Сгенерированный пароль должен отличаться от старого"
        response = user.update_info()
        assert response.success, "Сервер должен вернуть статус-код успешного изменения пароля"
        # Проверяем, что можно залогиниться с новым паролем
        user.logout()
        response = user.login()
        assert response.success, "Сервер должен вернуть статус-код входа"
        # Проверяем, что нельзя залогиниться со старым паролем
        user.logout()
        user.password = old_password
        response = user.login()
        assert response.success == False, "Авторизация по старому паролю должна стать невозможной"

    @pytest.mark.parametrize("field", ["email", "name", "password"])
    @allure.title("Изменение данных, когда пользователь разлогинился")
    def test_patch_user_info_when_user_is_logout(self, field, logout_stellar_burger_user):
        """Тест проверяет, что невозможно изменить данные пользователя, если пользователь разлогинился,
        но в запросе передан старый токен авторизации"""

        user = logout_stellar_burger_user
        available_attr = ["email", "name", "password"]
        assert field in available_attr, f"Недопустимое имя аттрибута: {field}. Допустимые аттрибуты: {available_attr}"
        old = {field: getattr(user, field)}
        method_name = f"generate_{field}"
        generate_method = getattr(user, method_name)
        generate_method()
        response = user.update_info()
        assert response.status_code == 401, ("Сервер не должен обновлять информацию, если пользователь разлогинился, "
                                             "т.к. токен авторизации должен быть сброшен")
