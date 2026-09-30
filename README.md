# Sprint_7 — финальный проект 7 спринта

Автотесты API учебного сервиса [Яндекс.Самокат](https://qa-scooter.praktikum-services.ru/).

Документация API: https://qa-scooter.praktikum-services.ru/docs/

## Стек

- Python 3
- pytest
- requests
- allure-pytest

## Структура проекта

```
Sprint_7/
├── urls.py                 # базовый URL и эндпоинты
├── data.py                 # тестовые данные и ожидаемые сообщения
├── helpers.py              # хелперы для запросов к API
├── conftest.py             # фикстуры (создание/удаление тестовых данных)
├── requirements.txt
├── pytest.ini
├── tests/
│   ├── test_create_courier.py   # тесты создания курьера
│   ├── test_login_courier.py    # тесты логина курьера
│   ├── test_create_order.py     # тесты создания заказа (с параметризацией)
│   └── test_list_orders.py      # тесты списка заказов
└── allure-report/          # сгенерированный Allure-отчёт
```

## Установка

```bash
pip3 install -r requirements.txt
```

Для просмотра Allure-отчёта нужен [Allure Commandline](https://docs.qameta.io/allure/).

## Запуск тестов

```bash
pytest
```

С генерацией результатов Allure:

```bash
pytest --alluredir=allure-results
```

## Allure-отчёт

Сгенерировать HTML-отчёт:

```bash
allure generate allure-results -o allure-report --clean
```

Открыть отчёт локально:

```bash
allure open allure-report
```

или:

```bash
allure serve allure-results
```

## Что покрыто тестами

1. **Создание курьера** — успешное создание, дубликат, отсутствие обязательных полей
2. **Логин курьера** — успешная авторизация, неверные данные, отсутствие полей, несуществующий пользователь
3. **Создание заказа** — параметризация по цвету (BLACK / GREY / оба / без цвета), наличие `track`
4. **Список заказов** — в теле ответа возвращается список заказов
