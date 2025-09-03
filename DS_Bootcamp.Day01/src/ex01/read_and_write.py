def csv_to_tsv(input_file, output_file):

    try:
        with open(input_file, 'r', encoding='utf-8') as csv_file:
            with open(output_file, 'w', encoding='utf-8') as tsv_file:
                for line in csv_file:
                    # Обработка строки вручную
                    result = []
                    in_quotes = False
                    current_field = ""

                    for char in line:
                        if char == '"':  # Обработка кавычек
                            in_quotes = not in_quotes
                            current_field += char
                        elif char == ',' and in_quotes == False:  # Разделитель вне кавычек
                            result.append(current_field)
                            current_field = ""
                        else:  # Обычный символ
                            current_field += char

                    # Добавляем последнее поле
                    if current_field:
                        result.append(current_field)

                    # Записываем результат с табуляциями вместо запятых
                    tsv_file.write('\t'.join(result))

                    # print(result)

        print("Конвертация файла завершена")
        return True

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False


if __name__ == "__main__":

    input_csv = "ds.csv"
    output_tsv = "ds.tsv"

    csv_to_tsv(input_csv, output_tsv)
