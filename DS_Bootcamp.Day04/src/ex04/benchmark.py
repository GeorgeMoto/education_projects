#!/usr/bin/env python3

import random
import sys
from timeit import timeit
from collections import Counter


def generate_random_list():
    return [random.randint(0, 100) for _ in range(1_000_000)]


def count_with_dict(data):
    result = {}
    for num in data:
        if num in result:
            result[num] += 1
        else:
            result[num] = 1
    return result


def count_with_counter(data):
    return Counter(data)


def top_10_with_dict(data):
    freq = count_with_dict(data)
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]


def top_10_with_counter(data):
    return Counter(data).most_common(10)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Необходимо запустить скрипт через команду ./benchmark.py")
        sys.exit(1)
    try:
        data = generate_random_list()

        my_count_time = timeit(lambda: count_with_dict(data), number=1)
        counter_time = timeit(lambda: count_with_counter(data), number=1)
        my_top_time = timeit(lambda: top_10_with_dict(data), number=1)
        counter_top_time = timeit(lambda: top_10_with_counter(data), number=1)

        print(f"my function: {my_count_time:.7f}")
        print(f"Counter: {counter_time:.7f}")
        print(f"my top: {my_top_time:.7f}")
        print(f"Counter's top: {counter_top_time:.7f}")

    except Exception as e:
        print(f"Ошибка: {e}")
