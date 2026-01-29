from collections import Counter
from pathlib import Path


class Movie:
    """Класс для представления фильма"""
    def __init__(self, identifier: str, title: str):
        self.identifier = identifier
        self.title = title
        self.watched = False

    def __str__(self) -> str:
        status = "✓" if self.watched else "○"
        return f"{status} {self.identifier}: {self.title}"

    def mark_as_watched(self):
        """Отмечает фильм как просмотренный"""
        self.watched = True


class MovieLibrary:
    """Класс для управления библиотекой фильмов"""
    def __init__(self):
        self.movie_collection = []  # Список всех фильмов
        self.movie_index = {}  # Быстрый доступ по ID
        self.view_counts = Counter()  # Подсчет просмотров
        self.viewing_history = []  # История просмотров пользователей

    def add_movie(self, movie_id: str, title: str):
        """Добавляет новый фильм в библиотеку"""
        if movie_id in self.movie_index:
            raise ValueError(f"Фильм с ID '{movie_id}' уже существует")

        new_movie = Movie(movie_id, title)
        self.movie_collection.append(new_movie)
        self.movie_index[movie_id] = new_movie

    def record_user_history(self, watched_movies: list):
        """Записывает историю просмотров пользователя"""
        watched_set = set(watched_movies)
        self.viewing_history.append(watched_set)

        # Обновляем счетчики просмотров
        for movie_id in watched_set:
            self.view_counts[movie_id] += 1

    def set_user_watched(self, movie_ids: list):
        """Устанавливает фильмы, просмотренные текущим пользователем"""
        for movie_id in map(str, movie_ids):
            if movie_id in self.movie_index:
                self.movie_index[movie_id].mark_as_watched()

    def find_similar_users(self, user_watched: set, threshold: float = 0.5):
        """Находит пользователей с похожими предпочтениями"""
        similar_users = []

        for history in self.viewing_history:
            common_movies = user_watched.intersection(history)
            similarity = len(common_movies) / len(user_watched) if user_watched else 0

            if similarity >= threshold:
                similar_users.append(history)

        return similar_users

    def generate_recommendation(self, watched_ids: list):
        """Генерирует рекомендацию на основе просмотренных фильмов"""
        if not watched_ids:
            return None

        # Преобразуем ID в строки и отмечаем как просмотренные
        watched_set = {str(mid) for mid in watched_ids}
        self.set_user_watched(watched_ids)

        # Находим похожих пользователей
        similar_users = self.find_similar_users(watched_set)

        if not similar_users:
            return None

        # Собираем кандидатов на рекомендацию
        candidate_movies = set()
        for history in similar_users:
            candidate_movies.update(history.difference(watched_set))

        if not candidate_movies:
            return None

        # Выбираем самый популярный фильм
        best_movie_id = max(
            candidate_movies,
            key=lambda mid: self.view_counts.get(mid, 0)
        )

        return self.movie_index.get(best_movie_id)

    def display_library(self):
        """Выводит всю библиотеку фильмов"""
        print("\n Библиотека фильмов:")
        for movie in sorted(self.movie_collection, key=lambda m: m.identifier):
            print(f"  {movie}")

    def load_from_files(self, movies_file: str, history_file: str):
        """Загружает данные из файлов"""
        movies_path = Path(movies_file)
        history_path = Path(history_file)

        # Загрузка фильмов
        with movies_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",", 1)
                    if len(parts) == 2:
                        movie_id, title = parts
                        self.add_movie(movie_id.strip(), title.strip())

        # Загрузка истории просмотров
        with history_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    watched_movies = [mid.strip() for mid in line.split(",")]
                    self.record_user_history(watched_movies)


def main():
    """Основная функция программы"""
    library = MovieLibrary()

    # Загрузка данных
    library.load_from_files("film.txt", "history.txt")

    # Получение ввода от пользователя
    print("Система рекомендаций фильмов")
    print("=" * 40)

    while True:
        user_input = input("\nВведите ID просмотренных фильмов через запятую (или 'выход'): ").strip()

        if user_input.lower() in ['выход', 'exit', 'quit']:
            break

        if not user_input:
            continue

        try:
            # Парсим ввод пользователя
            watched_ids = [mid.strip() for mid in user_input.split(",")]

            # Получаем рекомендацию
            recommendation = library.generate_recommendation(watched_ids)

            # Выводим результат
            print(f"\n Вы просмотрели: {', '.join(watched_ids)}")

            if recommendation:
                print(f" Рекомендуем к просмотру: {recommendation.title}")
            else:
                print(" Не удалось найти подходящую рекомендацию")

        except Exception as e:
            print(f" Ошибка: {e}")

    print("\n Спасибо за использование системы рекомендаций!")


if __name__ == "__main__":
    main()