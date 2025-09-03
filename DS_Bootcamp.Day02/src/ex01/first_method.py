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


class Research:
    file_name = "data.csv"

    def file_reader(self):
        with open(self.file_name, 'r') as file:
            return file.read()


if __name__ == '__main__':
    r1 = Research()
    print(r1.file_reader())
