import unittest
from src.sem1.lab3.sudoku import *


class SudokuCoreTests(unittest.TestCase):
    """Базовые тесты для функций судоку"""

    def test_group_function_basic(self):
        """Тест базовой функциональности группировки"""
        # Стандартные случаи
        self.assertEqual(group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
                         [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        # Граничные случаи
        self.assertEqual(group([], 5), [])
        self.assertEqual(group([10], 1), [[10]])
        self.assertEqual(group(['x', 'y'], 3), [['x', 'y']])

        # Несколько групп
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.assertEqual(group(letters, 4),
                         [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j']])

    def test_row_extraction_function(self):
        """Проверка извлечения строк"""
        test_board = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]

        # Проверяем все строки
        self.assertEqual(get_row(test_board, (0, 0)), ["1", "2", "3"])
        self.assertEqual(get_row(test_board, (1, 2)), ["4", "5", "6"])
        self.assertEqual(get_row(test_board, (2, 1)), ["7", "8", "9"])

        # С пустыми ячейками
        board_with_empty = [
            [".", "2", "."],
            ["4", ".", "6"],
            [".", "8", "."]
        ]
        self.assertEqual(get_row(board_with_empty, (0, 1)), [".", "2", "."])
        self.assertEqual(get_row(board_with_empty, (1, 0)), ["4", ".", "6"])

    def test_column_extraction_function(self):
        """Проверка извлечения столбцов"""
        sample_matrix = [
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"]
        ]

        # Проверяем все столбцы
        self.assertEqual(get_col(sample_matrix, (0, 0)), ["a", "d", "g"])
        self.assertEqual(get_col(sample_matrix, (1, 1)), ["b", "e", "h"])
        self.assertEqual(get_col(sample_matrix, (2, 2)), ["c", "f", "i"])

        # С цифрами и точками
        number_grid = [
            ["1", ".", "3"],
            [".", "5", "."],
            ["7", ".", "9"]
        ]
        self.assertEqual(get_col(number_grid, (0, 0)), ["1", ".", "7"])
        self.assertEqual(get_col(number_grid, (1, 1)), [".", "5", "."])
