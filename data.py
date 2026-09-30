# Тестовые данные и ожидаемые ответы API

# Сообщения об ошибках
COURIER_ALREADY_EXISTS_MESSAGE = 'Этот логин уже используется'
COURIER_NOT_ENOUGH_DATA_MESSAGE = 'Недостаточно данных для создания учетной записи'
LOGIN_NOT_ENOUGH_DATA_MESSAGE = 'Недостаточно данных для входа'
LOGIN_ACCOUNT_NOT_FOUND_MESSAGE = 'Учетная запись не найдена'

# Тело успешного создания курьера
COURIER_CREATED_BODY = {'ok': True}

# Базовое тело заказа без цвета (цвет добавляется в тестах)
ORDER_BODY = {
    'firstName': 'Naruto',
    'lastName': 'Uchiha',
    'address': 'Konoha, 142 apt.',
    'metroStation': 4,
    'phone': '+7 800 355 35 35',
    'rentTime': 5,
    'deliveryDate': '2020-06-06',
    'comment': 'Saske, come back to Konoha'
}

# Варианты цвета для параметризации создания заказа
ORDER_COLORS = [
    (['BLACK'], 'one_color_black'),
    (['GREY'], 'one_color_grey'),
    (['BLACK', 'GREY'], 'two_colors'),
    ([], 'no_color')
]
