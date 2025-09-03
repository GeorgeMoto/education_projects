#!/usr/bin/env python3
import sys
from functools import reduce
from timeit import timeit


def get_data_from_loop(number):
    value = 0
    for i in range(1, number+1):
        value += i*i
    return value


def get_data_from_reduce(number):
    value = reduce(lambda x, y: x + y*y, range(1, number+1))
    return value


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Необходимо запустить скрипт через команду ./benchmark.py <function_name> <number_of_iterations> <value>")
        sys.exit(1)

    try:
        function_name = sys.argv[1]
        number_of_iterations = int(sys.argv[2])
        value = int(sys.argv[3])

        if function_name == "loop":
            time_of_loop = timeit(lambda: get_data_from_loop(value), number=number_of_iterations)
            print(f"{time_of_loop:.7f}")
        elif function_name == "reduce":
            time_of_reduce = timeit(lambda: get_data_from_reduce(value), number=number_of_iterations)
            print(f"{time_of_reduce:.7f}")
        else:
            print("Необходимо передать в качестве аргумента одну из следующих функций: loop, reduce")
            sys.exit(1)

    except Exception as e:
        print(f"Ошибка: {e}")
