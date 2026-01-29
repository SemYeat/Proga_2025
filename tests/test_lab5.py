import unittest
from src.sem1.lab5.orders import *


class OrderValidationTestCase(unittest.TestCase):
    """Тесты для проверки валидации заказов"""

    def test_phone_number_validation(self):
        """Проверка валидации номеров телефонов"""
        validator = OrderValidator()

        # Корректные номера
        valid_phones = [
            "+7-928-417-13-40",
            "+1-234-567-89-01",
            "+44-123-456-78-90",
            "+375-123-456-78-90"
        ]

        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(
                    validator.validate_phone_number(phone),
                    f"Номер {phone} должен быть валидным"
                )

        # Некорректные номера
        invalid_phones = [
            "",  # пустая строка
            "89284171340",  # без +
            "+7-928-417-13",  # не хватает цифр
            "+7-92-417-13-40",  # неправильный формат
            "+7-928-41-13-40",  # неправильный формат
            "+7-928-417-1-40",  # неправильный формат
            "+7-928-417-13-4",  # неправильный формат
            "телефон",  # не цифры
            "+7-abc-def-gh-ij"  # буквы вместо цифр
        ]

        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertFalse(
                    validator.validate_phone_number(phone),
                    f"Номер {phone} должен быть невалидным"
                )

    def test_address_validation_basic(self):
        """Базовая проверка валидации адресов"""
        validator = OrderValidator()

        # Корректные адреса
        valid_addresses = [
            "Россия. Московская область. Москва. улица Пушкина",
            "Франция. Иль-де-Франс. Париж. Шанз-Элизе",
            "США. Калифорния. Лос-Анджелес. Голливудский бульвар",
            "Германия. Бавария. Мюнхен. Мариенплац 1",
            "Италия.Лацио.Рим.Колизей",  # без пробелов после точек
        ]

        for address in valid_addresses:
            with self.subTest(address=address):
                self.assertTrue(
                    validator.validate_address(address),
                    f"Адрес '{address}' должен быть валидным"
                )

        # Некорректные адреса
        invalid_addresses = [
            "",  # пустая строка
            "Россия",  # только страна
            "Россия. Москва",  # не хватает частей
            "Россия. Московская область. Москва",  # не хватает улицы
            "Россия. Московская область. Москва. улица Пушкина. дом 1. квартира 2",  # слишком много частей
        ]

        for address in invalid_addresses:
            with self.subTest(address=address):
                result = validator.validate_address(address)
                self.assertFalse(
                    result,
                    f"Адрес '{address}' должен быть невалидным, но был распознан как валидный"
                )


    def test_country_extraction(self):
        """Извлечение страны из адреса"""
        validator = OrderValidator()

        test_cases = [
            ("Россия. Московская область. Москва. улица Пушкина", "Россия"),
            ("Франция. Иль-де-Франс. Париж. Шанз-Элизе", "Франция"),
            ("США. Калифорния. Лос-Анджелес. Голливудский бульвар", "США"),
            ("Германия. Бавария. Мюнхен. Мариенплац", "Германия"),
            ("Великобритания. Англия. Лондон. Бейкер-стрит", "Великобритания"),
            ("", ""),  # пустой адрес
            ("Только страна", "Только страна"),  # нет точек
            ("Страна. Регион", "Страна"),  # меньше 4 частей
            ("Япония . Токио . Район . Улица", "Япония"),  # с пробелами вокруг точек
            ("  Россия  .  Москва  .  Улица  .  Дом  ", "Россия"),  # много пробелов
        ]

        for address, expected_country in test_cases:
            with self.subTest(address=address):
                extracted = validator.extract_country(address)
                self.assertEqual(
                    extracted, expected_country,
                    f"Для адреса '{address}' ожидалась страна '{expected_country}', получено '{extracted}'"
                )

    def test_priority_ranking(self):
        """Определение приоритета заказа"""
        validator = OrderValidator()

        test_cases = [
            ("MAX", 0),
            ("max", 0),  # регистр не должен иметь значения
            ("Max", 0),
            ("MIDDLE", 1),
            ("middle", 1),
            ("Middle", 1),
            ("LOW", 2),
            ("low", 2),
            ("Low", 2),
            ("", 3),  # неизвестный приоритет
            ("HIGH", 3),  # неизвестный приоритет
            ("medium", 3),  # неизвестный приоритет
            ("MIN", 3),  # неизвестный приоритет
            ("123", 3),  # числа
            ("МАКС", 3),  # русские буквы
            ("  MAX  ", 0),  # с пробелами
            ("  middle  ", 1),  # с пробелами
        ]

        for priority_str, expected_rank in test_cases:
            with self.subTest(priority=priority_str):
                rank = validator.get_priority_value(priority_str)
                self.assertEqual(
                    rank, expected_rank,
                    f"Для приоритета '{priority_str}' ожидался ранг {expected_rank}, получено {rank}"
                )