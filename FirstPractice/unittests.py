import unittest
from gnome_sort import sort

class TestGnomeSort(unittest.TestCase):
    
    def test_sort_ordinary_cases(self):
        """Тесты для обычных случаев"""
        self.assertEqual(sort([4, 2, 7, 1, 9, 3]), [1, 2, 3, 4, 7, 9])
        self.assertEqual(sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
    
    def test_sort_edge_cases(self):
        """Тесты для краевых случаев"""
        self.assertEqual(sort([]), [])
        self.assertEqual(sort([42]), [42])
    
    def test_sort_with_duplicates(self):
        """Тесты для повторяющихся элементов"""
        self.assertEqual(sort([5, 3, 8, 3, 2, 5]), [2, 3, 3, 5, 5, 8])
    
    def test_sort_floats(self):
        """Тесты для сортировки вещественных чисел"""
        self.assertEqual(sort([4.2, 2.1, 7.5, 1.0, 9.8]), [1.0, 2.1, 4.2, 7.5, 9.8])
    
    def test_sort_with_negative_numbers(self):
        """Тесты для сортировки с отрицательными числами"""
        self.assertEqual(sort([3, -1, -4, 2, 0]), [-4, -1, 0, 2, 3])
    
    def test_sort_mixed_neg_pos(self):
        """Тесты для смешанных отрицательных и положительных чисел"""
        self.assertEqual(sort([-3, 0, 2, -1, 4]), [-3, -1, 0, 2, 4])
    
    def test_sort_type_error(self):
        """Тесты для проверки ошибки TypeError"""
        with self.assertRaises(TypeError):
            sort("not a list")
    
    def test_sort_value_error(self):
        """Тесты для проверки ошибки ValueError при неверных элементах"""
        with self.assertRaises(ValueError):
            sort([1, 2, 'three', 4])

if __name__ == '__main__':
    unittest.main()
