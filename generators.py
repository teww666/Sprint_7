import random
import string


def generate_random_string(length=10):
    """Генерирует строку из строчных латинских букв заданной длины."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_courier_payload():
    """Генерирует уникальные данные курьера: login, password, firstName."""
    return {
        'login': generate_random_string(10),
        'password': generate_random_string(10),
        'firstName': generate_random_string(10)
    }
