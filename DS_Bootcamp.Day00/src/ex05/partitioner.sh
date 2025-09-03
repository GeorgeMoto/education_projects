#!/bin/sh

# Этот скрипт разделяет CSV файл на отдельные файлы по датам в поле created_at

# Используем известное имя файла
INPUT_FILE="hh_positions.csv"


# Проверяем исходник -f file
if [ ! -f $INPUT_FILE ]; then
    echo "Ошибка: Файл hh_positions.csv не найден"
    exit 1
fi


# Получаем заголовок CSV файла (первая строка)
HEADER=$(head -n 1 "$INPUT_FILE")

# Создаем директорию для временных файлов, -d директория 
TMP_DIR=$(mktemp -d)

# Обрабатываем каждую строку, кроме заголовка
tail -n +2 "$INPUT_FILE" | while IFS= read -r line; do
    # Извлекаем дату из поля created_at (формат YYYY-MM-DD), -o выводит только совпадение, а не всю строку
    DATE=$(echo "$line" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
    
    # Проверяем, что дата была извлечена корректно, -n == True if len(str) != 0 else False
    if [ -n "$DATE" ]; then
        # Создаем файл с заголовком, если он еще не существует
        if [ ! -f "$TMP_DIR/$DATE.csv" ]; then
            echo "$HEADER" > "$TMP_DIR/$DATE.csv"
        fi
        
        # Добавляем строку в соответствующий файл
        echo "$line" >> "$TMP_DIR/$DATE.csv"
    fi
done

# Выводим созданные файлы в текущую директорию, basename удаляет путь к директории из полного пути
for file in "$TMP_DIR"/*.csv; do
    FILENAME=$(basename "$file")
    cp "$file" "./$FILENAME"
done

# Очистка временных файлов
rm -rf "$TMP_DIR"

echo "Обработка файла завершена"