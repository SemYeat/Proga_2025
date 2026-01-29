class SurveyRespondent:
    """Класс для представления респондента опроса"""
    def __init__(self, full_name: str, age_years: int):
        self.full_name = full_name
        self.age_years = age_years

    def __lt__(self, other):
        """Для сортировки: сначала по возрасту (убывание), потом по имени (возрастание)"""
        if self.age_years == other.age_years:
            return self.full_name < other.full_name
        return self.age_years > other.age_years

    def __str__(self):
        return f"{self.full_name} ({self.age_years})"

    def __repr__(self):
        return f"Respondent('{self.full_name}', {self.age_years})"


class AgeCategory:
    """Класс для представления возрастной категории"""

    def __init__(self, lower_bound: int, upper_bound: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.respondents_list = []

    @property
    def label(self):
        """Возвращает текстовую метку категории"""
        if self.upper_bound >= 123:  # Последняя категория
            return f"{self.lower_bound}+"
        else:
            return f"{self.lower_bound}-{self.upper_bound}"

    def includes(self, age: int) -> bool:
        """Проверяет, попадает ли возраст в эту категорию"""
        return self.lower_bound <= age <= self.upper_bound

    def add_respondent(self, respondent: SurveyRespondent):
        """Добавляет респондента в категорию"""
        if self.includes(respondent.age_years):
            self.respondents_list.append(respondent)

    def sort_respondents(self):
        """Сортирует респондентов в категории"""
        self.respondents_list.sort()

    def is_empty(self) -> bool:
        """Проверяет, пустая ли категория"""
        return len(self.respondents_list) == 0

    def __str__(self):
        """Строковое представление категории"""
        if self.is_empty():
            return ""

        self.sort_respondents()
        respondents_str = ", ".join(str(r) for r in self.respondents_list)
        return f"{self.label}: {respondents_str}"


class AgeGroupManager:
    """Менеджер для управления возрастными группами"""
    MAX_AGE = 123  # Максимальный возраст по условию

    def __init__(self, boundaries: list[int]):
        self.boundaries = sorted(boundaries)
        self.categories = self._create_categories()

    def _create_categories(self) -> list[AgeCategory]:
        """Создает возрастные категории на основе границ"""
        categories = []

        # Начальная категория: от 0 до первой границы
        if self.boundaries:
            categories.append(AgeCategory(0, self.boundaries[0]))
        else:
            # Если границ нет, создаем одну категорию от 0 до MAX_AGE
            categories.append(AgeCategory(0, self.MAX_AGE))
            return categories

        # Промежуточные категории
        for i in range(len(self.boundaries) - 1):
            lower = self.boundaries[i] + 1
            upper = self.boundaries[i + 1]
            categories.append(AgeCategory(lower, upper))

        # Последняя категория: от последней границы+1 до MAX_AGE
        last_lower = self.boundaries[-1] + 1
        categories.append(AgeCategory(last_lower, self.MAX_AGE))

        return categories

    def add_respondent(self, name: str, age: int):
        """Добавляет респондента в подходящие категории"""
        if age < 0 or age > self.MAX_AGE:
            raise ValueError(f"Некорректный возраст: {age}")

        respondent = SurveyRespondent(name, age)

        for category in self.categories:
            category.add_respondent(respondent)

    def get_non_empty_categories(self) -> list[AgeCategory]:
        """Возвращает только непустые категории"""
        return [cat for cat in self.categories if not cat.is_empty()]

    def display_results(self):
        """Выводит результаты разбивки по категориям"""
        # Сортируем категории от старшей к младшей
        sorted_categories = sorted(
            self.get_non_empty_categories(),
            key=lambda cat: -cat.lower_bound
        )

        for category in sorted_categories:
            print(category)


def main():
    """Основная функция программы"""
    print(" Система разбивки респондентов по возрастным группам")
    print("=" * 50)

    try:
        # Чтение границ групп
        boundaries_input = input("Введите границы возрастных групп через пробел: ").strip()

        if boundaries_input:
            boundaries = list(map(int, boundaries_input.split()))
        else:
            boundaries = []
            print(" Границы не указаны, будет создана одна категория")

        manager = AgeGroupManager(boundaries)

        print("\nВведите данные респондентов в формате: Фамилия Имя Отчество, возраст")
        print("Для завершения ввода введите 'END'")
        print("-" * 50)

        # Чтение данных респондентов
        respondent_count = 0
        while True:
            try:
                input_line = input().strip()

                if input_line.upper() == "END":
                    break

                if not input_line:
                    continue

                # Парсим строку
                parts = input_line.split(", ", 1)
                if len(parts) != 2:
                    print(f" Ошибка формата: '{input_line}'")
                    continue

                name, age_str = parts

                try:
                    age = int(age_str)
                    manager.add_respondent(name, age)
                    respondent_count += 1
                except ValueError:
                    print(f" Некорректный возраст: '{age_str}'")

            except EOFError:
                break
            except Exception as e:
                print(f" Ошибка обработки: {e}")

        print(f"\n Обработано респондентов: {respondent_count}")
        print("\n Результаты разбивки по возрастным группам:")
        print("-" * 50)

        # Вывод результатов
        manager.display_results()

    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()