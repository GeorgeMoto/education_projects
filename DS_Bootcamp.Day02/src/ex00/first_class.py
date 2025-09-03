data_with_headers = (
    ("head", "tail"),
    (0, 1),
    (1, 0),
    (0, 1),
    (1, 0),
    (0, 1),
    (0, 1),
    (0, 1),
    (1, 0),
    (1, 0),
    (0, 1),
    (1, 0)
)

def create_csv(data):
    with open('data.csv', 'w') as file:
        for tup in data:
            data_for_csv = ",".join(map(str, tup))
            file.writelines(data_for_csv + "\n")

create_csv(data_with_headers)


class Must_read:
    file_name = "data.csv"
    with open(file_name, 'r') as file:
        for line in file.readlines():
            print(line, end="")


if __name__ == '__main__':
    Must_read()
