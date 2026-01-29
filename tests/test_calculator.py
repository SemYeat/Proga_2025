import unittest
from src.sem1.lab1.calculator import *

class CalculatorTestCase(unittest.TestCase):
    def test_addition(self):
        """Тест сложения"""
        self.assertEqual(calculate("+", 5, 3), 8)
        self.assertEqual(calculate("+", -5, 3), -2)
        self.assertEqual(calculate("+", 0, 0), 0)
        self.assertEqual(calculate("+", 2.5, 1.5), 4.0)

    def test_subtraction(self):
        """Тест вычитания"""
        self.assertEqual(calculate("-", 5, 3), 2)
        self.assertEqual(calculate("-", 3, 5), -2)
        self.assertEqual(calculate("-", 0, 5), -5)
        self.assertEqual(calculate("-", 5.5, 2.5), 3.0)

    def test_multiplication(self):
        """Тест умножения"""
        self.assertEqual(calculate("*", 5, 3), 15)
        self.assertEqual(calculate("*", -5, 3), -15)
        self.assertEqual(calculate("*", 0, 5), 0)
        self.assertEqual(calculate("*", 2.5, 4), 10.0)

    def test_division(self):
        """Тест деления"""
        self.assertEqual(calculate("/", 6, 3), 2.0)
        self.assertEqual(calculate("/", 5, 2), 2.5)
        self.assertEqual(calculate("/", -6, 3), -2.0)
        self.assertEqual(calculate("/", 0, 5), 0.0)

    def test_division_by_zero(self):
        """Тест деления на ноль"""
        with self.assertRaises(ValueError):
            calculate("/", 5, 0)

    def test_power(self):
        """Тест возведения в степень"""
        self.assertEqual(calculate("^", 2, 3), 8)
        self.assertEqual(calculate("^", 5, 0), 1)
        self.assertEqual(calculate("^", 3, 2), 9)
        self.assertEqual(calculate("^", 2, -1), 0.5)

    def test_modulo(self):
        """Тест остатка от деления"""
        self.assertEqual(calculate("%", 7, 3), 1)
        self.assertEqual(calculate("%", 10, 2), 0)
        self.assertEqual(calculate("%", 5, 5), 0)
        self.assertEqual(calculate("%", 8, 3), 2)

    def test_invalid_operation(self):
        """Тест неверной операции"""
        with self.assertRaises(ValueError):
            calculate("$", 5, 3)



