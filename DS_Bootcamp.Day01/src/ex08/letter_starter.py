# letter_starter.py
import sys


def start_letter(email):
    with open('employees.tsv', 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:  # Пропускаем заголовок
        data = line.strip().split('\t')
        print(data)
        if len(data) >= 3 and data[2] == email:
            name = data[0]
            return (f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. "
                    f"That's a precondition for the professionals that our company hires.")

    return "Email не найден в базе данных."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Некорректный запуск скрипта. Команда для запуска python3 letter_starter.py <путь к файлу>")
        sys.exit(1)

    letter = start_letter(sys.argv[1])
    print(letter)