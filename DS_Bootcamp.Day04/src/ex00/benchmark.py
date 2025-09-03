#!/usr/bin/env python3
from timeit import timeit
import sys


def get_data_from_loop():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.co',
              'anna@live.com', 'philipp@gmail.com']

    list_of_emails = emails * 5
    result = []

    for i in list_of_emails:
        result.append(i)

    return result


def get_data_from_list_comprehension():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.co',
              'anna@live.com', 'philipp@gmail.com']

    list_of_emails = emails * 5
    result = [i for i in list_of_emails]

    return result


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Необходимо запустить скрипт через команду ./benchmark.py")
        sys.exit(1)

    try:
        time_of_loop = timeit(get_data_from_loop, number=9000000)
        time_of_lc = timeit(get_data_from_list_comprehension, number=9000000)

        if time_of_loop < time_of_lc:
            print("It is better to use a loop")
            print(f"{time_of_loop} vs {time_of_lc}")
        else:
            print("It is better to use a list comprehension")
            print(f"{time_of_lc} vs {time_of_loop}")

    except Exception as e:
        print(f"Ошибка: {e}")


