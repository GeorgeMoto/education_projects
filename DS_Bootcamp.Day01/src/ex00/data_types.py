def data_types():
    #int, str, float, bool, list, dict, tuple, set

    num = 8
    char = "str"
    f_num = 8.0
    bl = True
    lst = []
    my_dict = {}
    my_tup = ()
    my_set = set()

    result = [num, char, f_num, bl, lst, my_dict, my_tup, my_set]

    type_names = list(map(lambda x: type(x).__name__, result))
    
    print(f"[{', '.join(type_names)}]")

if __name__ == '__main__':
    data_types()
