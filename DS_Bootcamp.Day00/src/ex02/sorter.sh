#!/bin/sh

# Проверяем исходник -f file
if [ ! -f hh.csv ]; then
    echo "Ошибка: Файл hh.csv не найден"
    exit 1
fi

# Сохраняем заголовок из первой строки
head -n 1 hh.csv > hh_sorted.csv

# Сортируем все строки, кроме заголовка, сначала по полю created_at (2), затем по id (1). -t разделитель
tail -n +2 hh.csv | sort -t',' -k2,2 -k1,1 >> hh_sorted.csv

echo "Сортировка завершена. Результат сохранен в файл hh_sorted.csv"