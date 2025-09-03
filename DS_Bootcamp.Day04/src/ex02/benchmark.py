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


def get_data_from_filter():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.co',
              'anna@live.com', 'philipp@gmail.com']

    list_of_emails = emails * 5
    result = filter(lambda x:x, list_of_emails)

    return result


def get_dict_of_functions():
    return {
        "loop": get_data_from_loop,
        "list_comprehension": get_data_from_list_comprehension,
        "map": get_data_from_map,
        "filter": get_data_from_filter
    }


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit(1)

    if len(sys.argv) != 3:
        print("Необходимо запустить скрипт через команду ./benchmark.py <function_name> <number>")
        sys.exit(1)

    try:
        function_name = sys.argv[1]
        number_of_iterations = int(sys.argv[2])
        dict_of_functions = get_dict_of_functions()
        print(get_data_from_filter())

        if function_name not in get_dict_of_functions():
            print(f'Необходимо передать в качестве аргумента одну из следующих '
                  f'функций: {", ".join(dict_of_functions.keys())}')
            sys.exit(1)
        functions = dict_of_functions[function_name]

        print(timeit(functions, number=number_of_iterations))

    except Exception as e:
        print(f"Ошибка: {e}")

