import sys


def string_decoder(work_type, input_text, index):

    def cipher(text, index, operation="encode"):

        result_string = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        # +1 для кодирования, -1 для декодирования *index
        op_sign = 1 if operation == "encode" else -1

        for char in text:
            if char.isalpha():

                if char.lower() not in alphabet:
                    raise Exception("Текст содержит символы кириллицы")

                if char.islower():
                    char_index = alphabet.index(char)
                    new_index = (char_index + op_sign * index) % 26
                    result_string += alphabet[new_index]
                else:
                    char_index = alphabet.index(char.lower())
                    new_index = (char_index + op_sign * index) % 26
                    result_string += alphabet[new_index].upper()
            else:
                result_string += char

        print(result_string)


    if work_type == "encode":
        cipher(input_text, index, "encode")

    elif work_type == "decode":
        cipher(input_text, index, "decode")
    else:
        raise Exception(
            f"Неверное название задачи {work_type}. Допустимые значения: encode, decode")


if __name__ == "__main__":
    try:
        # sys.arg = [название скрипта и аргумент]
        if len(sys.argv) != 4:
            raise Exception("Неверный формат ввода "
                            "Корректный формат: python3 caesar.py <режим работы encode/decode> <текст> <шаг>")

        #python3 caesar.py encode 'ssh -i private.key user@school21.ru' 1
        work_type = sys.argv[1]
        input_text = sys.argv[2]
        index = int(sys.argv[3])


        string_decoder(work_type, input_text, index)
    except Exception as e:
        print(f"Произошла ошибка: {e}")