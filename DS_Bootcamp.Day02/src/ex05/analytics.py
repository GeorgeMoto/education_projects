from random import randint


class Research:
    def __init__(self, path_to_file: str) -> None:
        self.path_to_file = path_to_file

    def file_reader(self, has_header: bool = True) -> list[list[int]]:
        try:
            with open(self.path_to_file, 'r') as file:
                content = file.read()
                lines = content.strip().split('\n')

                start_index = 1 if has_header else 0

                header = lines[0].split(',')
                if len(header) != 2:
                    raise Exception(
                        "Неверная структура файла: заголовок должен содержать 2 строки, разделенные запятой")

                list_of_values: list[list[int]] = []
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
        def __init__(self, data: list[list[int]]) -> None:
            self.data = data

        def counts(self) -> tuple[int, int]:
            heads_count, tails_count = 0, 0

            for item in self.data:
                heads_count += item[0]
                tails_count += item[1]

            return heads_count, tails_count

        def fractions(self, counts_tuple: tuple[int, int]) -> tuple[float, float]:
            heads = counts_tuple[0]
            tails = counts_tuple[1]
            values = heads + tails

            percent_of_heads = heads / values * 100
            percent_of_tails = tails / values * 100

            return percent_of_heads, percent_of_tails


class Analytics(Research.Calculations):
    def __init__(self, data: list[list[int]]) -> None:
        Research.Calculations.__init__(self, data)

    def predict_random(self, predictions_count: int) -> list[list[int]]:
        result = []
        for i in range(predictions_count):
            head_tail_generator = randint(0, 1)
            if head_tail_generator == 0:
                result.append([0, 1])
            else:
                result.append([1, 0])

        return result

    def predict_last(self) -> list[int]:
        return self.data[-1]

    def save_file(self, data: str, filename: str, extension: str) -> bool:
        # Проверка наличия аргументов
        if data is None or not isinstance(data, str):
            print("Ошибка: данные должны быть строкой")
            return False

        if filename is None or not isinstance(filename, str) or not filename:
            print("Ошибка: имя файла должно быть непустой строкой")
            return False

        if extension is None or not isinstance(extension, str) or not extension:
            print("Ошибка: расширение файла должно быть непустой строкой")
            return False

        try:
            with open(f"{filename}.{extension}", 'w') as file:
                file.write(data)
            return True
        except Exception as e:
            print(f"Непредвиденная ошибка при сохранении файла: {e}")
            return False

    def calculate_forecast(self, predictions: list[list[int]]) -> tuple[int, int]:
        forecast_heads = 0
        forecast_tails = 0
        for prediction in predictions:
            forecast_heads += prediction[0]
            forecast_tails += prediction[1]
        return forecast_heads, forecast_tails