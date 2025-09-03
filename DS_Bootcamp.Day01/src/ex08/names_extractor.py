# names_extractor.py
import sys


def extract_names(file_path):
    with open(file_path, 'r') as file:
        emails = file.read().strip().split('\n')
        print(emails)

    with open('employees.tsv', 'w') as output:
        output.write("Name\tSurname\tE-mail\n")

        for email in emails:
            # Извлекаем имя и фамилию из email
            name_surname = email.split('@')[0]
            name, surname = name_surname.split('.')

            # Делаем первую букву заглавной
            name = name.capitalize()
            surname = surname.capitalize()

            output.write(f"{name}\t{surname}\t{email}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Некорректный запуск скрипта. Команда для запуска python3 names_extractor.py <путь к файлу>")
        sys.exit(1)

    extract_names(sys.argv[1])