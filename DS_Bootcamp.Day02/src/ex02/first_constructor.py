import sys


class Research:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def file_reader(self):
        try:
            with open(self.path_to_file, 'r') as file:
                content = file.read()
                # Получаем список строк
                # ['head,tail', '0,1', '1,0', '0,1', '1,0'...]
                lines = content.strip().split('\n')

                # Проверка структуры файла
                if len(lines) < 2:  # Должен быть хотя бы заголовок и строка
                    raise Exception("Неверная структура файла: файл слишком короткий")

                header = lines[0].split(',')
                if len(header) != 2:
                    raise Exception(
                        "Неверная структура файла: заголовок должен содержать 2 строки, разделенные запятой")

                # Проверка строк данных
                for i in range(1, len(lines)):
                    data = lines[i].split(',')
                    if len(data) != 2:
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать 2 значения")
                    if data[0] not in ['0', '1'] or data[1] not in ['0', '1']:
                        raise Exception(f"Неверная структура файла: строка {i + 1} должна содержать только 0 или 1")
                    if data[0] == data[1]:
                        raise Exception(
                            f"Неверная структура файла: строка {i + 1} не должна содержать одинаковые значения")

                return content
        except FileNotFoundError:
            raise Exception(f"Файл {self.path_to_file} не найден")
        except Exception as e:
            raise e


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Ошибка: укажите путь к файлу в качестве аргумента")
        sys.exit(1)

    path_to_file = sys.argv[1]

    try:
        research = Research(path_to_file)
        data = research.file_reader()
        print(data, end='')  # Используем end='' чтобы избежать лишнего перевода строки
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
