from datetime import datetime
import sys
import time

# изменение лимита по рекурсии
sys.setrecursionlimit(2000)

# декоратор для измерения времени выполнения функции с помощью модуля time
def timer(func):
    def func(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter() - start
        print(f'Время выполнения функции: {end}')
        return result
    return func

# декоратор для измерения времени выполнения функции с помощью модуля datetime
def measure_time(func):
    def func(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now() - start
        print(f'Время выполнения функции: {end}')
        return result
    return func