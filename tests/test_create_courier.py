import allure

from helpers import create_courier, get_courier_id, delete_courier, generate_courier_payload
from data import (
    COURIER_CREATED_BODY,
    COURIER_ALREADY_EXISTS_MESSAGE,
    COURIER_NOT_ENOUGH_DATA_MESSAGE
)


@allure.epic('API Яндекс.Самокат')
@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать — код 201 и тело ok: true')
    @allure.description('Проверка успешного создания курьера с валидными данными')
    def test_create_courier_with_valid_data_returns_201_and_ok_true(self, courier_payload):
        response = create_courier(courier_payload)

        assert response.status_code == 201
        assert response.json() == COURIER_CREATED_BODY

        # очистка тестовых данных
        courier_id = get_courier_id(courier_payload['login'], courier_payload['password'])
        delete_courier(courier_id)

    @allure.title('Нельзя создать двух одинаковых курьеров — код 409')
    @allure.description('Повторное создание курьера с тем же логином возвращает ошибку')
    def test_create_courier_with_duplicate_login_returns_409(self, created_courier):
        duplicate_payload = {
            'login': created_courier['login'],
            'password': created_courier['password'],
            'firstName': created_courier['firstName']
        }

        response = create_courier(duplicate_payload)

        assert response.status_code == 409
        assert COURIER_ALREADY_EXISTS_MESSAGE in response.json()['message']

    @allure.title('Создание курьера без логина — код 400')
    @allure.description('Если не передать обязательное поле login, возвращается ошибка')
    def test_create_courier_without_login_returns_400(self):
        payload = generate_courier_payload()
        del payload['login']

        response = create_courier(payload)

        assert response.status_code == 400
        assert response.json()['message'] == COURIER_NOT_ENOUGH_DATA_MESSAGE

    @allure.title('Создание курьера без пароля — код 400')
    @allure.description('Если не передать обязательное поле password, возвращается ошибка')
    def test_create_courier_without_password_returns_400(self):
        payload = generate_courier_payload()
        del payload['password']

        response = create_courier(payload)

        assert response.status_code == 400
        assert response.json()['message'] == COURIER_NOT_ENOUGH_DATA_MESSAGE

    @allure.title('Создание курьера только с обязательными полями login и password — код 201')
    @allure.description(
        'Для создания курьера достаточно обязательных полей login и password; '
        'запрос возвращает ok: true'
    )
    def test_create_courier_with_only_required_fields_returns_201_and_ok_true(self):
        payload = generate_courier_payload()
        del payload['firstName']

        response = create_courier(payload)

        assert response.status_code == 201
        assert response.json() == COURIER_CREATED_BODY

        courier_id = get_courier_id(payload['login'], payload['password'])
        delete_courier(courier_id)
