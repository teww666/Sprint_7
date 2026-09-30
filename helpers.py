import random
import string
import time

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from urls import (
    CREATE_COURIER_URL,
    LOGIN_COURIER_URL,
    DELETE_COURIER_URL,
    CREATE_ORDER_URL,
    GET_ORDERS_URL,
    CANCEL_ORDER_URL
)


def _session_with_retries():
    """Сессия requests с повторными попытками при сбоях учебного стенда."""
    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.5,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE']),
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session


SESSION = _session_with_retries()


def generate_random_string(length=10):
    """Генерирует строку из строчных латинских букв заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_payload():
    """Генерирует уникальные данные курьера: login, password, firstName."""
    return {
        'login': generate_random_string(10),
        'password': generate_random_string(10),
        'firstName': generate_random_string(10)
    }


def _request_with_fallback(method, url, **kwargs):
    """
    Выполняет запрос с паузой и дополнительными ручными ретраями
    на ConnectionError (учебный стенд иногда рвёт соединение).
    """
    last_error = None
    for attempt in range(3):
        try:
            time.sleep(0.3)
            return SESSION.request(method, url, timeout=20, **kwargs)
        except requests.exceptions.RequestException as error:
            last_error = error
            time.sleep(1 * (attempt + 1))
    raise last_error


@allure.step('Регистрация нового курьера')
def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает список [login, password, firstName].
    Если регистрация не удалась, возвращает пустой список.
    """
    login_pass = []
    payload = generate_courier_payload()

    response = _request_with_fallback('POST', CREATE_COURIER_URL, data=payload)

    if response.status_code == 201:
        login_pass.append(payload['login'])
        login_pass.append(payload['password'])
        login_pass.append(payload['firstName'])

    return login_pass


@allure.step('Создание курьера')
def create_courier(payload):
    """Отправляет POST /api/v1/courier с переданным телом."""
    return _request_with_fallback('POST', CREATE_COURIER_URL, data=payload)


@allure.step('Логин курьера')
def login_courier(payload):
    """Отправляет POST /api/v1/courier/login с переданным телом."""
    return _request_with_fallback('POST', LOGIN_COURIER_URL, data=payload)


@allure.step('Получение id курьера по логину и паролю')
def get_courier_id(login, password):
    """Возвращает id курьера или None, если логин неуспешен."""
    response = login_courier({'login': login, 'password': password})
    if response.status_code == 200:
        return response.json().get('id')
    return None


@allure.step('Удаление курьера по id')
def delete_courier(courier_id):
    """Отправляет DELETE /api/v1/courier/:id."""
    if courier_id is None:
        return None
    return _request_with_fallback('DELETE', f'{DELETE_COURIER_URL}/{courier_id}')


@allure.step('Создание заказа')
def create_order(payload):
    """Отправляет POST /api/v1/orders с переданным телом."""
    return _request_with_fallback('POST', CREATE_ORDER_URL, json=payload)


@allure.step('Получение списка заказов')
def get_orders():
    """Отправляет GET /api/v1/orders."""
    return _request_with_fallback('GET', GET_ORDERS_URL)


@allure.step('Отмена заказа по track')
def cancel_order(track):
    """
    Отправляет PUT /api/v1/orders/cancel.
    Важно: track передаётся в URL-параметрах (params), а не в теле запроса —
    в документации ручек 2 и 3 это указано неверно.
    """
    if track is None:
        return None
    return _request_with_fallback('PUT', CANCEL_ORDER_URL, params={'track': track})
