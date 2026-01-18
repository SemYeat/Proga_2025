import os
import shutil
import stat
import time
import psutil
import platform


"""Задание 1"""
import os.path


def task1():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = os.getcwd()

    """Проверяем текущ директорию"""
    if script_dir != curr_dir:
        print(f'Перемещаемся из {curr_dir} в {script_dir}')
        os.chdir(script_dir)

    """1. Создаём файл"""
    file_my = os.path.join(os.getcwd(), "os_file.txt")
    with open(file_my, 'w') as z:
        z.write("Я люблю вкусно покушать! \nСтрока 2 \n Строка 3")

    """2. Проверяем сущ файла"""
    if os.path.exists(file_my):
        print(f'Файл {file_my} создан')
    else:
        print('Ошибка файл не создан')
        return
    """3. Инфа о файле"""
    stat_file = os.stat(file_my)
    print(f"Размер файла: {stat_file.st_size}")
    print(f"Дата послелнего изменения: {time.ctime(stat_file.st_mtime)}")
    print(f"Дата последнего доступа: {time.ctime(stat_file.st_atime)}")

    """4. Тикущий пользователь"""
    print(f"Текущий пользователь: {os.getlogin()}")

    """5. Права доступа"""
    print(f"Текущие права доступа: {oct(stat_file.st_mode)[-3:]}")
    """Меняем права на (владелец, группа, чтение, запись, выполнение)"""
    os.chmod(file_my, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    new_stat = os.stat(file_my)
    print(f"Новые права доступа:{oct(new_stat.st_mode)[-3:]}")

if __name__ == "__main__":
    task1()

"""Задание 2"""

def task2():
    """1. Копирование файла"""
    orig_file = "os_file.txt"
    copy_file = "os_file_copy.txt"
    shutil.copy2(orig_file, copy_file)

    """2. Переименовение и перемещен файл"""
    new_name = "rename_os_file.txt"
    os.rename(copy_file, new_name)
    """Вложенные директории"""
    nest_dir = os.path.join("dir1", "dir2", "dir3")
    os.makedirs(nest_dir, exist_ok=True)
    """Перемещаем файл"""
    move_file = os.path.join((nest_dir, "move_file.txt"))
    os.rename(new_name, move_file)

    """3. Создание. Перемещение и переменовение одной командой"""
    new_file = "second_file.txt"
    with open(new_file, "w") as f:
        f.write("Задание 2 пункт 3")
        "Два действия одной командой"
        os.rename(new_file, os.path.join("dir1", "final_file.txt"))

    """4. Создание нескол файлов и вывод содержимого (Сложный кайф)"""
    for i in range(3):
        with open(f" tesk2_file{i}.txt", "w") as z:
            z.write(f"Файл номер {i}")
    print("\n Содержимое текущ директории:")
    for i in os.listdir():
        print(f"{i} - {"дирекрория" if os.path.isdir(i) else "файл"}")

        """Переходим во вложенную дир"""
    os.chdir(nest_dir)
    print("\n Содержимое текущ директории:")
    for i in os.listdir():
        print(i)

    """5. Возврат в нач. Создание пустой дир, удаление её. Создание ещё нескольких вложенных директорий и файлов"""
    """Возврат"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    """Созд и удален пустой дир"""
    empty_dir = "empty_dir"
    os.mkdir(empty_dir)
    os.rmdir(empty_dir)

    """Создаём вложенные дир и файлов """
    big_dir = os.path.join("deep", "deeper", "deepest")
    os.makedirs(big_dir)
    for i in range(2):
        with open(os.path.join(big_dir, f"deep_file{i}.txt"), "w") as t:
            t.write(f"Файл на глубине {i}")

    """6. Обход дир"""
    print("\n Обход дир")
    for glavn, dir, files in os.walk("."):
        print(f"\n Директория: {glavn}")
        print("Поддиректории:" .join(dir) if dir else "нет")
        print("Файлы:" .join(files) if files else "no")
if __name__ == "__main__":
    task2()

"""Задание 3 (10/10 Кайф. Стоит запомнить)"""
def running_proces():
    """Показываем список всех запущенных процессов"""
    print("\n Список запущенных процессов:")
    for i in psutil.process_iter(["pid","name","username"]):
        try:
            print(f"PID:{i.info["pid"]}, Имя:{i.info["name"]}, Пользователь:{i.info["username"]}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def proces_detl(pid):
    """Показываем детальную инфу о процессе"""
    try:
        z = psutil.Process(pid)
        print(f"\nДетали процесса{pid}")
        print(f" Имя{z.name()}")
        print(f"Статус{z.status()}")
        print(f"Пользователь{z.username()}")
        print(f"Запущен{z.ctime(z.create_time())}")
        print(f"Исп СPU{z.cpu_percent()}")
        print(f"Использует памяти{z.memory_info().rss}")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {pid} не найден")
    except psutil.AccessDenied:
        print(f"Нет прав доступа процесса {pid}")

def stop_proces(p):
    try:
        z = psutil.Process(p)
        z.terminate()
        print(f"Процесс {p} ({z.name()}) завершен")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {p} не найден")
    except psutil.AccessDenied:
        print(f"Нет прав доступа процесса {p}")

def environment_variables():
    """Показать или добавить переменные окружения"""
    print("\n Текущие переменные окружения")
    for key, znach in os.environ.items():
        print(f"{key} -- {znach}")
    print("\n Добавить новую переменную окружение (для ВЫХОДА оставте  имя ПУСТЫМ)")
    while True:
        key = input("Имя переменной: ").strip()
        if not key:
            break
        znach = input("Значение: ").strip()
        os.environ[key] = znach
        print(f"Переменная {key} с знач {znach} добавлена")

def chen_prior(i, prioretet):
    """Изменить приоритет процесса"""
    try:
        i = psutil.Process(i)
        i.nice(prioretet)
        print(f"Приоритет процесса {i} изменён на {prioretet}")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {i} не найден")
    except psutil.AccessDenied:
        print(f"Нет прав доступа процесса {i}")

def sys_info():
    "Информация о системе"
    print(f"\n OC:{platform.system()}{platform.release()}")
    print(f"Версия:{platform.version()}")
    print(f"Архитектура:{platform.machine()}")
    print(f"Имя компа:{platform.node()}")
    print(f"Пользователь:{platform.getloin()}")
    print(f"Процессор:{platform.processor()}")
    print(f"Тикущая дир:{os.getcwd()}")


def task3():
    """Интерактивное меню для управления системой"""
    menu = """
        Меню управления системой:
        a) Список всех запущенных процессов
        b) Детали процесса
        c) Завершить процесс
        d) Переменные окружения
        e) Изменить приоритет процесса
        f) Информация о системе
        g) Выход
        """
    while True:
        print(menu)
        chil = input("Выберите опцию (a-g):").lower().strip()
        if chil == "a":
            running_proces()
        elif chil == "b":
            proces_detl()
        elif chil == "c":
            stop_proces()
        elif chil == "d":
            environment_variables()
        elif chil == "e":
            chen_prior()
        elif chil == "f":
            sys_info()
        elif chil == "g":
            print("Выход")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main":
   task3()