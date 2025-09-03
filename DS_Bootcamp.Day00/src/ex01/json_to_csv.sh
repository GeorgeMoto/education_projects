#!/bin/sh

# Проверяем существование исходников
if [ ! -f hh.json ]; then
    echo "Ошибка: Файл hh.json не найден"
    exit 1
fi


if [ ! -f filter.jq ]; then
    echo "Ошибка: Файл filter.jq не найден"
    exit 1
fi

# Создаем заголовок CSV-файла
echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > hh.csv

# Применяем filter.jq для преобразования JSON в CSV, сырые строки плюс фильтр с файла
jq -r -f filter.jq hh.json >> hh.csv

echo "Конвертация завершена. Результат сохранен в файл hh.csv"