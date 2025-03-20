BASE_URL = "https://stellarburgers.nomoreparties.site"


class ApiEndpoints:
    register = f"{BASE_URL}/api/auth/register"
    user = f"{BASE_URL}/api/auth/user"
    login = f"{BASE_URL}/api/auth/login"
    logout = f"{BASE_URL}/api/auth/logout"
    ingredients = f"{BASE_URL}/api/ingredients"
    orders = f"{BASE_URL}/api/orders"