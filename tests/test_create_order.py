import allure
import pytest

from helpers import create_order, cancel_order
from data import ORDER_BODY, ORDER_COLORS


@allure.epic('API Яндекс.Самокат')
@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с разными вариантами цвета — код 201 и поле track')
    @allure.description(
        'Заказ можно создать: с одним цветом (BLACK или GREY), '
        'с двумя цветами и без указания цвета. В ответе возвращается track.'
    )
    @pytest.mark.parametrize('color, case_name', ORDER_COLORS)
    def test_create_order_with_different_colors_returns_201_and_track(self, color, case_name):
        payload = ORDER_BODY.copy()
        if color:
            payload['color'] = color

        response = create_order(payload)

        assert response.status_code == 201
        assert 'track' in response.json()

        # очистка тестовых данных
        cancel_order(response.json().get('track'))
