#!/bin/sh

# Проверяем исходник -f file
if [ ! -f hh_sorted.csv ]; then
    echo "Ошибка: Файл hh_sorted.csv не найден"
    exit 1
fi

# Копируем заголовок
head -n 1 hh_sorted.csv > hh_positions.csv

# Обрабатываем остальные строки, через while построчно, IFS пишет строку целиком
# без сепаратора, т.к. пустая, в переменную line
tail -n +2 hh_sorted.csv | while IFS= read -r line
do
    # Извлекаем все части строки, cut -d',' разделитель
    id=$(echo "$line" | cut -d',' -f1)
    created=$(echo "$line" | cut -d',' -f2)
    name=$(echo "$line" | cut -d',' -f3)
    rest=$(echo "$line" | cut -d',' -f4-)
    
    # Убираем кавычки из имени для проверки + нижний регистр
    name_clean=$(echo "$name" | tr -d '"')
    name_lower=$(echo "$name_clean" | tr '[:upper:]' '[:lower:]')
    
    # Проверяем наличие ключевых слов, -q для возврата статуса без значения.
    position="-"
    
    if echo "$name_lower" | grep -q "junior"; then
        if echo "$name_lower" | grep -q "middle"; then
            if echo "$name_lower" | grep -q "senior"; then
                position="Junior/Middle/Senior"
            else
                position="Junior/Middle"
            fi
        elif echo "$name_lower" | grep -q "senior"; then
            position="Junior/Senior"
        else
            position="Junior"
        fi
    elif echo "$name_lower" | grep -q "middle"; then
        if echo "$name_lower" | grep -q "senior"; then
            position="Middle/Senior"
        else
            position="Middle"
        fi
    elif echo "$name_lower" | grep -q "senior"; then
        position="Senior"
    fi
    
    # Формируем новую строку и записываем в выходной файл
    echo "$id,\"$created\",\"$position\",$rest" >> hh_positions.csv
done

echo "Очистка завершена. Результат сохранен в файл hh_positions.csv"