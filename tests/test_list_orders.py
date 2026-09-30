import allure

from helpers import get_orders


@allure.epic('API Яндекс.Самокат')
@allure.feature('Список заказов')
class TestListOrders:

    @allure.title('Получение списка заказов — код 200 и список в теле ответа')
    @allure.description('В теле ответа возвращается список заказов в поле orders')
    def test_get_orders_list_returns_200_and_orders_list(self):
        response = get_orders()

        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)
