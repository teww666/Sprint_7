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


def _request(method, url, **kwargs):
    """Выполняет запрос через сессию с ретраями (см. _session_with_retries)."""
    return SESSION.request(method, url, timeout=20, **kwargs)


@allure.step('Создание курьера')
def create_courier(payload):
    """Отправляет POST /api/v1/courier с переданным телом."""
    return _request('POST', CREATE_COURIER_URL, data=payload)


@allure.step('Логин курьера')
def login_courier(payload):
    """Отправляет POST /api/v1/courier/login с переданным телом."""
    return _request('POST', LOGIN_COURIER_URL, data=payload)


@allure.step('Получение id курьера по логину и паролю')
def get_courier_id(login, password):
    """Возвращает id курьера или None, если в ответе нет id (логин неуспешен)."""
    response = login_courier({'login': login, 'password': password})
    return response.json().get('id')


@allure.step('Удаление курьера по id')
def delete_courier(courier_id):
    """Отправляет DELETE /api/v1/courier/:id."""
    return _request('DELETE', f'{DELETE_COURIER_URL}/{courier_id}')


@allure.step('Создание заказа')
def create_order(payload):
    """Отправляет POST /api/v1/orders с переданным телом."""
    return _request('POST', CREATE_ORDER_URL, json=payload)


@allure.step('Получение списка заказов')
def get_orders():
    """Отправляет GET /api/v1/orders."""
    return _request('GET', GET_ORDERS_URL)


@allure.step('Отмена заказа по track')
def cancel_order(track):
    """
    Отправляет PUT /api/v1/orders/cancel.
    Важно: track передаётся в URL-параметрах (params), а не в теле запроса —
    в документации ручек 2 и 3 это указано неверно.
    """
    return _request('PUT', CANCEL_ORDER_URL, params={'track': track})
