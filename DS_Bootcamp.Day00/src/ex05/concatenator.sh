#!/bin/sh

# Выходной файл
OUTPUT_FILE="result.csv"

# Находим все CSV файлы по дате в текущей директории
CSV_FILES=$(find . -maxdepth 1 -name "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv" | sort)

# Получаем первый файл из списка
FIRST_FILE=$(echo "$CSV_FILES" | head -1)

# Получаем заголовок из первого файла и записываем в выходной файл
head -n 1 "$FIRST_FILE" > "$OUTPUT_FILE"

# Обрабатываем все найденные CSV файлы
for file in $CSV_FILES; do
    # Добавляем все строки кроме заголовка из текущего файла в выходной файл
    tail -n +2 "$file" >> "$OUTPUT_FILE"
done

# Сортировка файла с сохранением заголовка
# Создаем временный файл для сортировки
TMP_FILE=$(mktemp)

# Копируем заголовок
head -n 1 "$OUTPUT_FILE" > "$TMP_FILE"

# Добавляем отсортированные данные
tail -n +2 "$OUTPUT_FILE" | sort -t',' -k2,2 -k1,1 >> "$TMP_FILE"

# Заменяем исходный файл отсортированным
mv "$TMP_FILE" "$OUTPUT_FILE"

echo "Данные отсортированы в файле $OUTPUT_FILE"