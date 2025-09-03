import sys
from random import randint


class Research:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def file_reader(self, has_header=True):
        try:
            with open(self.path_to_file, 'r') as file:
                content = file.read()
                lines = content.strip().split('\n')

                start_index = 1 if has_header else 0

                header = lines[0].split(',')
                if len(header) != 2:
                    raise Exception(
                        "Неверная структура файла: заголовок должен содержать 2 строки, разделенные запятой")

                list_of_values = []
                # Проверка строк данных
                for i in range(start_index, len(lines)):
                    data = lines[i].split(',')
                    if len(data) != 2:
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать 2 значения")
                    if data[0] not in ['0', '1'] or data[1] not in ['0', '1']:
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать только 0 или 1")
                    if data[0] == data[1]:
                        raise Exception(
                            f"Неверная структура файла: строка {i + 1} не должна содержать одинаковые значения")
                    list_of_values.append([int(data[0]), int(data[1])])

                return list_of_values
        except FileNotFoundError:
            raise Exception(f"Файл {self.path_to_file} не найден")
        except Exception as e:
            raise e

    class Calculations:
        def counts(self, list_of_data):
            heads_count, tails_count = 0, 0

            for data in list_of_data:
                heads_count += data[0]
                tails_count += data[1]

            return heads_count, tails_count

        def fractions(self, counts_tuple):
            heads = counts_tuple[0]
            tails = counts_tuple[1]
            values = heads + tails

            percent_of_heads = heads / values * 100
            percent_of_tails = tails / values * 100

            return percent_of_heads, percent_of_tails


class Analytics(Research.Calculations):
    def __init__(self, data):
        self.data = data

    def predict_random(self, predictions_count):
        result = []
        for i in range(predictions_count):
            head_tail_generator = randint(0, 1)
            if head_tail_generator == 0:
                result.append([0, 1])
            else:
                result.append([1, 0])

        return result

    def predict_last(self):
        return self.data[-1]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Ошибка: укажите путь к файлу в качестве аргумента")
        sys.exit(1)

    path_to_file = sys.argv[1]

    try:
        # Создаем объект Research и получаем данные
        research = Research(path_to_file)
        data = research.file_reader()
        print(data)

        # Создаем объект Calculations и вызываем его методы
        calc = research.Calculations()
        counts_result = calc.counts(data)
        print(counts_result[0], counts_result[1])

        # Вызываем метод fractions и выводим результат
        fractions_result = calc.fractions(counts_result)
        print(fractions_result[0], fractions_result[1])

        # Создаем объект Analytics с данными
        analytics = Analytics(data)

        # Получаем случайные предсказания (3 шага)
        random_predictions = analytics.predict_random(3)
        print(random_predictions)

        # Получаем последнее предсказание
        last_prediction = analytics.predict_last()
        print(last_prediction)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)