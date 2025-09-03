import sys

def get_data_of_clients(data_name):
    # текущие клиенты
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']

    # участник с мероприятия
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']

    # клиенты посмотревшие последнее письмо
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    def get_data_for_call_center():
        clients_for_call_center = list(set(clients) - set(recipients))
        return clients_for_call_center

    def get_data_of_potential_clients():
        potential_clients = list(set(participants) - set(clients))
        return potential_clients

    def get_data_for_loyalty_program():
        clients_for_loyalty_program = list(set(clients) - set(participants))
        return clients_for_loyalty_program

    if data_name == "call_center":
        result = get_data_for_call_center()
        print(result)
        return result
    elif data_name == "potential_clients":
        result = get_data_of_potential_clients()
        print(result)
        return result
    elif data_name == "loyalty_program":
        result = get_data_for_loyalty_program()
        print(result)
        return result
    else:
        raise Exception(
            f"Неверное название задачи {data_name}. Допустимые значения: call_center, potential_clients, loyalty_program")


if __name__ == "__main__":
    try:
        # sys.arg = [название скрипта и аргумент]
        if len(sys.argv) != 2:
            raise Exception("Требуется один аргумент для передачи в скрипт")

        task_name = sys.argv[1]
        get_data_of_clients(task_name)
    except Exception as e:
        print(f"Произошла ошибка: {e}")