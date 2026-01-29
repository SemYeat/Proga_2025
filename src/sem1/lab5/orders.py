from pathlib import Path
import re


class OrderValidator:
    # Регулярное выражение для проверки телефона
    PHONE_PATTERN = r'^\+\d{1,3}-\d{3}-\d{3}-\d{2}-\d{2}$'

    # Приоритеты для сортировки
    PRIORITY_LEVELS = {"MAX": 0, "MIDDLE": 1, "LOW": 2}

    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Проверяет корректность номера телефона"""
        if not phone:
            return False
        return bool(re.fullmatch(OrderValidator.PHONE_PATTERN, phone.strip()))

    @staticmethod
    def validate_address(address: str) -> bool:
        """Проверяет корректность адреса"""
        if not address:
            return False
        parts = [part.strip() for part in address.split('.')]
        return len(parts) == 4

    @staticmethod
    def extract_country(address: str) -> str:
        """Извлекает страну из адреса"""
        if not address:
            return ""
        parts = address.split('.', 1)
        return parts[0].strip() if parts else ""

    @staticmethod
    def get_priority_value(priority: str) -> int:
        """Возвращает числовое значение приоритета для сортировки"""
        priority_upper = priority.strip().upper()
        return OrderValidator.PRIORITY_LEVELS.get(priority_upper, 3)

    @staticmethod
    def format_product_list(products: str) -> str:
        """Форматирует список продуктов: подсчитывает количество"""
        items = [item.strip() for item in products.split(',')]
        item_counts = {}

        for item in items:
            item_counts[item] = item_counts.get(item, 0) + 1

        formatted_items = []
        for item, count in item_counts.items():
            if count > 1:
                formatted_items.append(f"{item} x{count}")
            else:
                formatted_items.append(item)

        return ', '.join(formatted_items)

    @staticmethod
    def format_address_for_output(address: str) -> str:
        """Форматирует адрес для вывода (убирает страну)"""
        if not address:
            return ""
        parts = [part.strip() for part in address.split('.')]
        # Пропускаем первый элемент (страну)
        return '. '.join(parts[1:]) if len(parts) > 1 else ""


def main():
    input_file = Path("orders.txt")
    valid_orders_file = Path("order_country.txt")
    invalid_orders_file = Path("non_valid_orders.txt")

    validator = OrderValidator()
    valid_orders = []
    invalid_entries = []

    # Чтение и валидация заказов
    with input_file.open("r", encoding="utf-8") as infile:
        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Разделение строки на поля
                fields = [field.strip() for field in line.split(';')]
                if len(fields) != 6:
                    continue

                order_id, products, customer, address, phone, priority = fields

                # Проверка адреса
                if not validator.validate_address(address):
                    error_address = address if address else "no data"
                    invalid_entries.append(f"{order_id};1;{error_address}")

                # Проверка телефона
                if not validator.validate_phone_number(phone):
                    error_phone = phone if phone else "no data"
                    invalid_entries.append(f"{order_id};2;{error_phone}")

                # Если все проверки пройдены, добавляем в список валидных
                if validator.validate_address(address) and validator.validate_phone_number(phone):
                    valid_orders.append({
                        'original_line': line,
                        'order_id': order_id,
                        'products': products,
                        'customer': customer,
                        'address': address,
                        'phone': phone,
                        'priority': priority,
                        'country': validator.extract_country(address)
                    })

            except Exception as e:
                print(f"Ошибка обработки строки {line_num}: {e}")

    # Сохранение невалидных заказов
    with invalid_orders_file.open("w", encoding="utf-8") as outfile:
        for entry in invalid_entries:
            outfile.write(entry + "\n")

    # Сортировка валидных заказов
    # Сначала заказы из России, потом по алфавиту стран, потом по приоритету
    def sort_key(order):
        country = order['country']
        is_russia = 0 if country.lower() == 'россия' else 1
        priority_val = validator.get_priority_value(order['priority'])
        return (is_russia, country, priority_val)

    valid_orders.sort(key=sort_key)

    # Сохранение отсортированных валидных заказов
    with valid_orders_file.open("w", encoding="utf-8") as outfile:
        for order in valid_orders:
            # Форматирование вывода
            formatted_products = validator.format_product_list(order['products'])
            formatted_address = validator.format_address_for_output(order['address'])

            output_line = f"{order['order_id']};{formatted_products};{order['customer']};{formatted_address};{order['phone']};{order['priority']}"
            outfile.write(output_line + "\n")

    print(f"Обработано {len(valid_orders)} валидных заказов")
    print(f"Найдено {len(invalid_entries)} ошибок")


if __name__ == "__main__":
    main()