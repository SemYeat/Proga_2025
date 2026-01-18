import asyncio
import time
import threading
import asyncio
import aiohttp
from asyncio import timeout, create_task
from turtledemo.penrose import start

import requests
from requests import session

"""Задание 1"""
async def delay1(delay, mes):
    await asyncio.sleep(delay)
    return mes


"""Задание 2"""
async def parallel_mess():
    results = await asyncio.gather(
        delay1(2, "Сообщение 2 сек"),
        delay1(1, "Сообщение 1 сек"),
        delay1(3, "Сообщение 3 сек"),
    )
    for r in results:
        print(r)
    return results

"""Задание 3"""
def sync_req():
    """Синхронные запросы"""
    urls = ["https://google.com", "https://youtube.com", "https://github.com"]
    start = time.time()
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            print(url - response.status_code - time.time() - start)
        except Exception as e:
            print(f"{url} -Ошибка {str(e)}")
    print(time.time() - start)

async def async_req():
    """Асинхронные запросы"""
    urls = ["https://google.com", "https://youtube.com", "https://github.com"]
    start = time.time()
    async with aiohttp.ClientSession() as session:
        t = []
        for url in urls:
            t = asyncio.create_task(f_url(session, url, start))
            t.append(t)
        await asyncio.gather(*t)
    print(time.time() - start)

async def f_url(session, url, start_time):
    try:
        async with session.get(url, timeout=5) as response:
            print(response.status - time.time() - start_time)
    except Exception as e:
        print(f"{url} - Ошибка {str(e)}")

"""Задание 4"""
"""delay - это задержка в сек"""
def print_message(message, delay):
    time.sleep(delay)
    print(message)
"""Синхронный запуск"""
def run_sync():
    stat = time.time()
    print_message("Я 1", 1)
    print_message("Я 2", 1)
    print_message("Я 3", 1)
    """Время синхронизации"""
    print(time.time() - stat)

"""Многопоточный запуск"""
def run_threaded():
    stat = time.time()
    threads = [ threading.Thread(target=print_message, args=("Поток 1", 1)),
        threading.Thread(target=print_message, args=("Поток 2", 1)),
        threading.Thread(target=print_message, args=("Поток 3", 1))]
    """Запускаем потоки паралельно"""
    for i in threads:
        i.start()
    """Ожидене завершения потока"""
    for i in threads:
        i.join()
    """Время выполнения всех потоков"""
    print(time.time() - stat)

"""Задание 5"""
un_count = 0

def unsafe():
    global un_count
    for i in range(1000000):
        un_count += 1
""""""
def f():
    global un_count
    un_count = 0
    threads = [threading.Thread(target=unsafe) for i in range(5)]
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    """Результат меньше 5000000 из-за гонки данных"""
    print(un_count)

"""Задание 6"""

"""Функзия с защитой гонки данных"""

def safe(count, lock):
    for _ in range(1000000):
        """Блокируем доступ"""
        with lock:
            count[0] += 1
def ff():
    count = [0]
    lock = threading.Lock()
    threads = [threading.Thread(target=safe, args=(count, lock)) for _ in range(5)]

    for i in threads:
        i.start()
    for i in threads:
        i.join()

    """Результат будет равен 5000000"""
    print(count)