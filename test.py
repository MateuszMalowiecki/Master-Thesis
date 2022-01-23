dict={(1, 2) : 3, (4, 5, 6) : 7, (8, 9) : (10, 11)}
for key, value in dict.items():
    print("-----------")
    if len(key) == 3:
        (first, second, third) = key
        print(first)
        print(second)
        print(third)
        print(value)
    elif len(key) == 2 and isinstance(value, tuple):
        (first, second) = key
        print(first)
        print(second)
        print(value)