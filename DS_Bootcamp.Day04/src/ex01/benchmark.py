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

def get_data_from_map():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.co',
              'anna@live.com', 'philipp@gmail.com']

    list_of_emails = emails * 5
    result = map(lambda x:x, list_of_emails)

    return result



if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Необходимо запустить скрипт через команду ./benchmark.py")
        sys.exit(1)

    try:
        time_of_loop = timeit(get_data_from_loop, number=9000000)
        time_of_lc = timeit(get_data_from_list_comprehension, number=9000000)
        time_of_map = timeit(get_data_from_map, number=9000000)

        values = sorted([time_of_loop, time_of_lc, time_of_map])
        info = f"{values[0]} vs {values[1]} vs {values[2]}"

        if time_of_map < time_of_lc and time_of_map < time_of_loop:
            print("It is better to use a map")
            print(info)
        elif time_of_lc < time_of_loop and time_of_lc < time_of_map:
            print("It is better to use a list comprehension")
            print(info)
        else:
            print("It is better to use a loop")
            print(info)

    except Exception as e:
        print(f"Ошибка: {e}")


