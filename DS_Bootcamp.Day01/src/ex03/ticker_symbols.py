import sys

def get_price_info(ticker_name=None):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }


    if ticker_name is None:
        return False

    ticker_name_upper = ticker_name.upper()

    # Проверяем, есть ли тикер в словаре STOCKS
    if ticker_name_upper in STOCKS:
        # Находим название компании по тикеру
        company_name = None
        for company, ticker in COMPANIES.items():
            if ticker == ticker_name_upper:
                company_name = company
                break

        price = STOCKS[ticker_name_upper]
        print(f"{company_name} {price}")
        return True
    else:
        print("Unknown ticker")
        return False


if __name__ == "__main__":
    args = sys.argv[1:]  # Получаем аргументы командной строки, исключая имя скрипта; for ex ['TESLA']

    # Проверяем количество аргументов
    if len(args) != 1:
        sys.exit(1)  # Завершаем программу с кодом ошибки 1 без вывода в консоль

    # Вызываем функцию если аргумент был один, args это lst
    result = get_price_info(args[0])

    # Если функция вернула False, завершаем программу с ошибкой
    if not result:
        sys.exit(1) # Завершаем программу с кодом ошибки 1 без вывода в консоль