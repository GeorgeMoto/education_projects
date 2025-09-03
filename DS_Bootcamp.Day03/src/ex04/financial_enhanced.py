#!/usr/bin/env python3
import sys
import time
import urllib.request
from bs4 import BeautifulSoup
import cProfile
import pstats


def get_financial_data(ticker, field_name):
    # time.sleep(5)
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        raise Exception(f"URL не существует или недоступен: {e}")

    soup = BeautifulSoup(html, 'html.parser')
    total_revenue_row = soup.find('div', attrs={'title': field_name})

    if total_revenue_row:
        parent_row = total_revenue_row.find_parent('div', class_='row')
        if parent_row:
            return tuple(cell.text.strip() for cell in parent_row.find_all('div', class_='column') if cell.text.strip())
        raise Exception("Не удалось найти строку данных для поля.")
    raise Exception(f"Поле '{field_name}' не найдено на странице")


def run_profiling(ticker, field):
    # 1. Профилирование для pstats-cumulative.txt
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        result = get_financial_data(ticker, field)
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.strip_dirs().sort_stats('cumtime')
        with open('pstats-cumulative.txt', 'w') as f:
            stats.stream = f
            stats.print_stats(5)

    # 2. Профилирование для profiling-html.txt (sort by tottime)
    with open('profiling-html.txt', 'w') as f:
        profiler = cProfile.Profile()
        profiler.enable()
        get_financial_data(ticker, field)
        profiler.disable()
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs().sort_stats('tottime').print_stats()

    # 3. Профилирование для profiling-ncalls.txt (sort by ncalls)
    with open('profiling-ncalls.txt', 'w') as f:
        profiler = cProfile.Profile()
        profiler.enable()
        get_financial_data(ticker, field)
        profiler.disable()
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs().sort_stats('ncalls').print_stats()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Формат запуска скрипта должен выглядеть так: python3 financial.py <ticker> <field_name>")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]

    run_profiling(ticker, field)