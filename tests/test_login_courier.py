import allure

from helpers import login_courier
from generators import generate_courier_payload
from data import (
    LOGIN_NOT_ENOUGH_DATA_MESSAGE,
    LOGIN_ACCOUNT_NOT_FOUND_MESSAGE
)


@allure.epic('API Яндекс.Самокат')
@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Курьер может авторизоваться — код 200 и поле id')
    @allure.description('Успешная авторизация созданного курьера возвращает id')
    def test_login_courier_with_valid_credentials_returns_200_and_id(self, created_courier):
        payload = {
            'login': created_courier['login'],
            'password': created_courier['password']
        }

        response = login_courier(payload)

        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] == created_courier['id']

    @allure.title('Авторизация без логина — код 400')
    @allure.description('Если не передать обязательное поле login, возвращается ошибка')
    def test_login_courier_without_login_returns_400(self, created_courier):
        # Пустая строка вместо отсутствия поля — единообразно с тестом без пароля
        payload = {
            'login': '',
            'password': created_courier['password']
        }

        response = login_courier(payload)

        assert response.status_code == 400
        assert response.json()['message'] == LOGIN_NOT_ENOUGH_DATA_MESSAGE

    @allure.title('Авторизация без пароля — код 400')
    @allure.description('Если не передать обязательное поле password, возвращается ошибка')
    def test_login_courier_without_password_returns_400(self, created_courier):
        # Пустая строка вместо отсутствия поля: без password учебный стенд зависает
        payload = {
            'login': created_courier['login'],
            'password': ''
        }

        response = login_courier(payload)

        assert response.status_code == 400
        assert response.json()['message'] == LOGIN_NOT_ENOUGH_DATA_MESSAGE

    @allure.title('Авторизация с неверным паролем — код 404')
    @allure.description('При неверном пароле система возвращает ошибку')
    def test_login_courier_with_wrong_password_returns_404(self, created_courier):
        payload = {
            'login': created_courier['login'],
            'password': 'wrong_password'
        }

        response = login_courier(payload)

        assert response.status_code == 404
        assert response.json()['message'] == LOGIN_ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title('Авторизация с неверным логином — код 404')
    @allure.description('При неверном логине система возвращает ошибку')
    def test_login_courier_with_wrong_login_returns_404(self, created_courier):
        payload = {
            'login': 'nonexistent_login_xyz',
            'password': created_courier['password']
        }

        response = login_courier(payload)

        assert response.status_code == 404
        assert response.json()['message'] == LOGIN_ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title('Авторизация под несуществующим пользователем — код 404')
    @allure.description('Если пользователя нет в системе, возвращается ошибка')
    def test_login_courier_with_nonexistent_user_returns_404(self):
        payload = generate_courier_payload()
        del payload['firstName']

        response = login_courier(payload)

        assert response.status_code == 404
        assert response.json()['message'] == LOGIN_ACCOUNT_NOT_FOUND_MESSAGE
