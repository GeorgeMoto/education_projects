#!/bin/sh

# Файл для анализа
INPUT_FILE="hh_positions.csv"

# Проверяем исходник -f file
if [ ! -f $INPUT_FILE ]; then
    echo "Ошибка: Файл hh_positions.csv не найден"
    exit 1
fi

# Создаем заголовок для выходного файла
echo 'name, count' > hh_uniq_positions.csv

# Подсчитываем позиции через поиск по ключевому слову, wc -l считает вхождения, -i игнорит регистр
JUNIOR_COUNT=$(grep -i "junior" "$INPUT_FILE" | wc -l)
MIDDLE_COUNT=$(grep -i "middle" "$INPUT_FILE" | wc -l)
SENIOR_COUNT=$(grep -i "senior" "$INPUT_FILE" | wc -l)

# Записываем результаты в файл
echo '"Junior", '"$JUNIOR_COUNT" >> hh_uniq_positions.csv
echo '"Middle", '"$MIDDLE_COUNT" >> hh_uniq_positions.csv
echo '"Senior", '"$SENIOR_COUNT" >> hh_uniq_positions.csv

echo "Статистика сохранена в файл hh_uniq_positions.csv"