import time


def work_time(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f'Запрос обрабатывался {t2} секунд')

    return wrapper
