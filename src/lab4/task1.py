from collections import defaultdict
from pathlib import Path


class Film:
    def __init__(self, id, name, viving):
        self.id = id
        self.name = name
        self.viving = viving
    def __str__(self):
        self.




class Library:
    def __init__(self):
        self.film_popularity = defaultdict(int)
        self.films = []
        self.films_dict = {}
        self.viewed_films = set()
        self.all_history = []

    def add_film(self, film_id, film_name):
        """Добавляет новый фильм в библиотеку"""
        if film_id not in self.films_dict:
            film = Film(film_id, film_name)
            self.films.append(film)
            self.films_dict[film_id] = film
        else: raise ValueError(f"id: {film_id} уже занято")

    def get_film(self, film_id) -> Film | None:
        """Возвращает фильм по ID"""
        return self.films_dict.get(film_id)

    def watch_film(self, film_id):
        """отмечает фильм просмотренным и добавляет его в viewed_films"""
        film_id = str(film_id)
        self.films_dict[film_id].viewing = True
        self.viewed_films.add(film_id)

    def add_all_history(self, film_ids):
        """Добавляет список просмотренных фильмов юзеров в all_history и считает кол-во просмотров фильма"""
        film_set = set(film_ids)
        self.all_history.append(film_set)

        for film_id in film_set:
            self.film_popularity[film_id] += 1

    def recommend_film(self) -> Film | None:
        if not self.viewed_films:
            return None

        target_viewed = self.viewed_films
        probable_films = set()
        # отбираем юзеров с совпадением >= 50%
        for user_history in self.all_history:
            intersection = target_viewed & user_history
            if len(intersection) >= len(target_viewed) / 2:
                probable_films.update(user_history - target_viewed)
        # выбираем самый популярный фильм
        if not probable_films:
            return None

        recommended_id = max(probable_films, key=lambda x: self.film_popularity.get(x, 0))
        return self.films_dict.get(recommended_id)

    def show_library(self):
        for film in self.films:
            print(film)


film_path = Path("film.txt")
history_path = Path("history.txt")
libr = Library()

with film_path.open("r", encoding="utf-8") as f:
    for line in f:
        id, name = map(str.strip, line.strip().split(","))
        libr.add_film(id, name)

with history_path.open("r", encoding="utf-8") as f:
    for line in f:
        libr.add_all_history(line.strip().split(","))


libr.watch_film(2)
libr.watch_film(4)
print(libr.recommend_film())
