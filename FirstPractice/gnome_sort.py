def sort(array):
    if not isinstance(array, list):  # --аргумент является списком--
        raise TypeError("Аргумент должен быть списком")
    
    if not all(isinstance(x, (int, float)) for x in array):  # --проверка, что все элементы списка числа--
        raise ValueError("Все элементы списка должны быть числами")

    index = 0
    while index < len(array):
        if index == 0 or array[index] >= array[index - 1]:
            index += 1
        else:
            array[index], array[index - 1] = array[index - 1], array[index]
            index -= 1
    return array

