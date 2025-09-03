#!/usr/bin/env python3
import sys
import time
import os
import resource


def get_peak_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)  # перевод в ГБ


def read_file_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: ./generator.py <file.csv>")
        sys.exit(1)

    file_path = sys.argv[1]

    start_time = time.time()
    lines_generator = read_file_generator(file_path)

    # Перебираем все строки, используя генератор, и вызываем pass
    for line in lines_generator:
        pass

    end_time = time.time()
    execution_time = end_time - start_time

    peak_memory = get_peak_memory_usage()

    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {execution_time:.2f}s")