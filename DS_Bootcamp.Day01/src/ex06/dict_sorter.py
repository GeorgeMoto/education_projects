def convert_list_to_dictionary():

    result = dict()

    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    result = {}
    for country, number in list_of_tuples:
        result[country] = int(number)

    # Сортируем список стран, лямбда приняла аргумент country  вернула tuple(value, key)
    sorted_countries = sorted(result, key=lambda country: (-result[country], country))

    for country in sorted_countries:
        print(country)

if __name__ == "__main__":
    convert_list_to_dictionary()