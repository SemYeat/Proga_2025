class Respondent:
    def __init__(self, name, years):
        self.full_name = name
        self.years = years

    def __lt__(self, other):
        if self.years == other.years:
            return self.name < other.name
        return self.years > other.years

    def __str__(self):
        return f"{self.name} ({self.years})"

    def __repr__(self):
        return f"Respondent('{self.name}', {self.years})"


class AgeCategory:
    def __init__(self, min_a, max_a):
        self.min_a = min_a
        self.max_a = max_a
        self.respondents = []

    def add_respondent(self, respondent):
        if self.min_a <= respondent.years <= self.max_a:
            self.respondents.append(respondent)

    def sort_respondents(self):
        self.respondents.sort()

    def __str__(self):
        if not self.respondents:
            return ""

        sorted_list = sorted(self.respondents)
        respondents_str = ", ".join(str(r) for r in sorted_list)

        if self.max_a == 123:
            return f"{self.min_a}+: {respondents_str}"
        else:
            return f"{self.min_a}-{self.max_a}: {respondents_str}"


class AgeGroupManager:
    def __init__(self, boundaries):
        self.boundaries = sorted(boundaries)
        self.categories = self._initialize_categories()

    def _initialize_categories(self):
        categories = []
        previous_bound = -1

        for bound in self.boundaries:
            categories.append(AgeCategory(previous_bound + 1, bound))
            previous_bound = bound

        last_category = AgeCategory(self.boundaries[-1] + 1, 123)
        categories.append(last_category)
        return categories

    def add_respondent(self, name, age):
        person = Respondent(name, age)
        for category in self.categories:
            category.add_respondent(person)

    def display_categories(self):
        # Сортируем категории от старшей к младшей
        sorted_categories = sorted(
            self.categories,
            key=lambda cat: -cat.lower
        )

        for category in sorted_categories:
            if category.respondents:
                category.sort_respondents()
                print(category)


def main():
    # Чтение границ возрастных групп
    try:
        bounds_input = input().strip()
        if bounds_input:
            boundaries = list(map(int, bounds_input.split()))
        else:
            boundaries = []
    except ValueError:
        print("Ошибка: введите числовые границы через пробел")
        return

    manager = AgeGroupManager(boundaries)

    while True:
        try:
            line = input().strip()
            if line == "END":
                break

            if line:
                parts = line.split(", ")
                if len(parts) == 2:
                    name, age_str = parts
                    try:
                        age = int(age_str)
                        manager.add_respondent(name, age)
                    except ValueError:
                        print(f"Ошибка: неверный возраст '{age_str}'")
                else:
                    print(f"Ошибка: неверный формат строки '{line}'")
        except EOFError:
            break

    # Вывод результатов
    manager.display_categories()


if __name__ == "__main__":
    main()