import pytest

from helpers import (
    create_courier,
    get_courier_id,
    delete_courier,
    create_order,
    cancel_order
)
from data import ORDER_BODY
from generators import generate_courier_payload


@pytest.fixture
def created_courier():
    """
    Создаёт курьера перед тестом и удаляет его после.
    Возвращает словарь с login, password, firstName и id.
    """
    payload = generate_courier_payload()
    response = create_courier(payload)
    assert response.status_code == 201, f'Не удалось создать курьера: {response.text}'

    courier_id = get_courier_id(payload['login'], payload['password'])
    courier_data = {
        'login': payload['login'],
        'password': payload['password'],
        'firstName': payload['firstName'],
        'id': courier_id
    }

    yield courier_data

    delete_courier(courier_data['id'])


@pytest.fixture
def created_order():
    """
    Создаёт заказ перед тестом и отменяет его после.
    Возвращает track заказа.
    """
    payload = ORDER_BODY.copy()
    payload['color'] = ['BLACK']
    response = create_order(payload)
    assert response.status_code == 201, f'Не удалось создать заказ: {response.text}'
    track = response.json().get('track')

    yield track

    cancel_order(track)
