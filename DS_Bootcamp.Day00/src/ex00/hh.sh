#!/bin/sh

# + используется вместо пробела для корректной передачи запроса через URL.
SEARCH_QUERY="data+scientist"

# Выполнение запроса к API HeadHunter, тихий режим и заголвок.
RESPONSE=$(curl -s -H "User-Agent: HH-User-Agent" "https://api.hh.ru/vacancies?text=${SEARCH_QUERY}&per_page=20")

# Проверка запроса.
if [ $? -ne 0 ]; then
    echo "Ошибка: Не удалось выполнить запрос к API HH."
    exit 1
fi

#jq формирует json, "." для структуры.
echo "$RESPONSE" | jq '.' > hh.json

echo "Информация о вакансиях 'data scientist' сохранена в файл hh.json"