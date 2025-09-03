#!/usr/bin/env python3
import sys
import time
import requests
from bs4 import BeautifulSoup


def get_financial_data(ticker, field_name):
    time.sleep(5)
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL не существует или недоступен: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')

    total_revenue_row = soup.find('div', attrs={'title': field_name})

    if total_revenue_row:
        parent_row = total_revenue_row.find_parent('div', class_='row')

        if parent_row:
            data_cells = parent_row.find_all('div', class_='column')

            revenue_values = []
            for cell in data_cells:
                if cell.text and cell.text.strip():
                    revenue_values.append(cell.text.strip())
            return tuple(revenue_values)

        else:
            raise Exception("Не удалось найти строку данных для поля.")
    else:
        raise Exception(f"Поле '{field_name}' не найдено на странице")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Формат запуска скрипта должен выглядеть так: python3 financial.py <ticker> <field_name>")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]

    try:
        result = get_financial_data(ticker, field)
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
