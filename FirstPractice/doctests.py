from gnome_sort import sort

def gnome_sort_doc_tests(array):
    """
    Тесты для функции сортировки методом гномьей сортировки.

    Обычные случаи:
    
    >>> sort([4, 2, 7, 1, 9, 3])
    [1, 2, 3, 4, 7, 9]

    >>> sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]

    >>> sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]

    Пустой список:

    >>> sort([])
    []

    Один элемент:

    >>> sort([42])
    [42]

    Повторяющиеся элементы:

    >>> sort([5, 3, 8, 3, 2, 5])
    [2, 3, 3, 5, 5, 8]

    Вещественные числа:

    >>> sort([4.2, 2.1, 7.5, 1.0, 9.8])
    [1.0, 2.1, 4.2, 7.5, 9.8]

    Отрицательные числа:

    >>> sort([3, -1, -4, 2, 0])
    [-4, -1, 0, 2, 3]

    Смешанные отрицательные и положительные числа:

    >>> sort([-3, 0, 2, -1, 4])
    [-3, -1, 0, 2, 4]

    Ошибочные случаи:

    Несоответствие типов:

    >>> sort("not a list")
    Traceback (most recent call last):
        ...
    TypeError: Аргумент должен быть списком

    Несоответствие типов элементов:

    >>> sort([1, 2, 'three', 4])
    Traceback (most recent call last):
        ...
    ValueError: Все элементы списка должны быть числами

    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
