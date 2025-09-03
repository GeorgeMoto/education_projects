from random import randint
import requests
from config import logger, telegram_bot_token, telegram_channel_id


class Research:
    def __init__(self, path_to_file: str) -> None:
        logger.info(f"Инициализация объекта Research с файлом {path_to_file}")
        self.path_to_file = path_to_file

    def file_reader(self, has_header: bool = True) -> list[list[int]]:
        logger.info(f"Чтение файла {self.path_to_file} с параметром has_header={has_header}")
        try:
            with open(self.path_to_file, 'r') as file:
                content = file.read()
                lines = content.strip().split('\n')

                start_index = 1 if has_header else 0

                header = lines[0].split(',')
                if len(header) != 2:
                    logger.error("Неверная структура файла: заголовок должен содержать 2 строки, разделенные запятой")
                    raise Exception(
                        "Неверная структура файла: заголовок должен содержать 2 строки, разделенные запятой")

                list_of_values: list[list[int]] = []
                # Проверка строк данных
                for i in range(start_index, len(lines)):
                    data = lines[i].split(',')
                    if len(data) != 2:
                        logger.error(f"Неверная структура файла: строка {i + 1} должна содержать 2 значения")
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать 2 значения")
                    if data[0] not in ['0', '1'] or data[1] not in ['0', '1']:
                        logger.error(f"Неверная структура файла: строка {i + 1} должна содержать только 0 или 1")
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать только 0 или 1")
                    if data[0] == data[1]:
                        logger.error(
                            f"Неверная структура файла: строка {i + 1} не должна содержать одинаковые значения")
                        raise Exception(
                            f"Неверная структура файла: строка {i + 1} не должна содержать одинаковые значения")
                    list_of_values.append([int(data[0]), int(data[1])])

                logger.info(f"Успешно прочитан файл, получено {len(list_of_values)} записей")
                return list_of_values
        except FileNotFoundError:
            logger.error(f"Файл {self.path_to_file} не найден")
            raise Exception(f"Файл {self.path_to_file} не найден")
        except Exception as e:
            logger.error(f"Ошибка при чтении файла: {e}")
            raise e

    def send_telegram_notification(self, success: bool) -> bool:
        logger.info("Отправка уведомления в Telegram")
        message = "The report has been successfully created" if success else "The report hasn't been created due to an error"

        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": telegram_channel_id,
            "text": message
        }

        try:
            response = requests.post(url, json=payload)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("ok"):
                logger.info("Уведомление успешно отправлено в Telegram")
                return True
            else:
                error_description = response_data.get("description", "Неизвестная ошибка")
                logger.error(f"Ошибка при отправке уведомления: {error_description}")
                return False
        except Exception as e:
            logger.error(f"Исключение при отправке уведомления: {e}")
            return False

    class Calculations:
        def __init__(self, data: list[list[int]]) -> None:
            logger.info("Инициализация объекта Calculations")
            self.data = data

        def counts(self) -> tuple[int, int]:
            logger.info("Подсчет количества орлов и решек")
            heads_count, tails_count = 0, 0

            for item in self.data:
                heads_count += item[0]
                tails_count += item[1]

            logger.info(f"Подсчитано: {heads_count} орлов и {tails_count} решек")
            return heads_count, tails_count

        def fractions(self, counts_tuple: tuple[int, int]) -> tuple[float, float]:
            logger.info("Расчет процентного соотношения орлов и решек")
            heads = counts_tuple[0]
            tails = counts_tuple[1]
            values = heads + tails

            percent_of_heads = heads / values * 100
            percent_of_tails = tails / values * 100

            logger.info(f"Рассчитаны проценты: {percent_of_heads:.2f}% орлов и {percent_of_tails:.2f}% решек")
            return percent_of_heads, percent_of_tails


class Analytics(Research.Calculations):
    def __init__(self, data: list[list[int]]) -> None:
        logger.info("Инициализация объекта Analytics")
        Research.Calculations.__init__(self, data)

    def predict_random(self, predictions_count: int) -> list[list[int]]:
        result = []
        for i in range(predictions_count):
            head_tail_generator = randint(0, 1)
            if head_tail_generator == 0:
                result.append([0, 1])
            else:
                result.append([1, 0])

        logger.info(f"Сгенерировано {len(result)} предсказаний")
        return result

    def predict_last(self) -> list[int]:
        logger.info("Получение последнего наблюдения для предсказания")
        logger.info(f"Получено предсказание: {self.data[-1]}")
        return self.data[-1]

    def save_file(self, data: str, filename: str, extension: str) -> bool:
        logger.info(f"Сохранение данных в файл {filename}.{extension}")
        # Проверка наличия аргументов
        if data is None or not isinstance(data, str):
            logger.error("Ошибка: данные должны быть строкой")
            print("Ошибка: данные должны быть строкой")
            return False

        if filename is None or not isinstance(filename, str) or not filename:
            logger.error("Ошибка: имя файла должно быть непустой строкой")
            print("Ошибка: имя файла должно быть непустой строкой")
            return False

        if extension is None or not isinstance(extension, str) or not extension:
            logger.error("Ошибка: расширение файла должно быть непустой строкой")
            print("Ошибка: расширение файла должно быть непустой строкой")
            return False

        try:
            with open(f"{filename}.{extension}", 'w') as file:
                file.write(data)
            logger.info(f"Файл {filename}.{extension} успешно сохранен")
            return True
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при сохранении файла: {e}")
            print(f"Непредвиденная ошибка при сохранении файла: {e}")
            return False

    def calculate_forecast(self, predictions: list[list[int]]) -> tuple[int, int]:
        forecast_heads = 0
        forecast_tails = 0
        for prediction in predictions:
            forecast_heads += prediction[0]
            forecast_tails += prediction[1]
        logger.info(f"Прогноз: {forecast_heads} орлов и {forecast_tails} решек")
        return forecast_heads, forecast_tails