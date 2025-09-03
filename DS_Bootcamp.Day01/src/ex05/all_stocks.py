import sys

#python3 all_stocks.py 'TSLA , aPPle, Facebook'
#TSLA is a ticker symbol for Tesla
#Apple stock price is 287.73
#Facebook is an unknown company or an unknown ticker symbol


def get_price_info(companys_name=None):
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

    if companys_name is None:
        return False

    # Проверка на две запятые подряд
    if ",," in companys_name:
        return False

    list_of_companies = companys_name.split(",")

    # Проверка на пустые элементы
    if "" in list_of_companies:
        return False

    for comp in list_of_companies:
        comp = comp.strip()  # Удаляем пробелы по краям

        if not comp:  # Пропускаем пустые строки
            return False

        # Проверяем, является ли компания тикером
        for company_name, ticker in COMPANIES.items():
            if comp.upper() == ticker:
                print(f"{comp.upper()} is a ticker symbol for {company_name}")
                break
        else:
            # Проверяем, является ли компания названием компании
            company_match = None
            for company in COMPANIES:
                if comp.lower() == company.lower():
                    company_match = company
                    break

            if company_match:
                ticker = COMPANIES[company_match]
                price = STOCKS[ticker]
                print(f"{company_match} stock price is {price}")
            else:
                print(f"{comp} is an unknown company or an unknown ticker symbol")

    return True


if __name__ == "__main__":
    args = sys.argv[1:]  # Получаем аргументы командной строки, исключая имя скрипта
    print(args)

    # Проверяем количество аргументов
    if len(args) != 1:
        sys.exit(1)  # Завершаем программу с кодом ошибки 1 без вывода в консоль

    # Вызываем функцию если аргумент был один
    result = get_price_info(args[0])

    # Если функция вернула False, завершаем программу с ошибкой
    if not result:
        sys.exit(1)  # Завершаем программу с кодом ошибки 1 без вывода в консоль