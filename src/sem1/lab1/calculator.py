def calculator():
    print("Операции")
    print("+")
    print("-")
    print("*")
    print("/")
    print("^")
    print("%")

    while True:
        oper = input("Введите операцию (или 'выход' для завершения): ")

        if oper.lower() == 'выход':
            print("Калькулятор завершает работу.")
            break

        if oper not in ["+", "-", "*", "/", "^", "%"]:
            print("Неверная операция")
            continue

        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
        except ValueError:
            print("Неверно. Введите числа")
            continue

        if oper == "+":
            rez = num1 + num2
        elif oper == "-":
            rez = num1 - num2
        elif oper == "*":
            rez = num1 * num2
        elif oper == "/":
            if num2 == 0:
                print("Деление на ноль")
                continue
            else:
                rez = num1 / num2
        elif oper == "^":
            rez = num1 ** num2
        elif oper == "%":
            rez = num1 % num2

        print(f" {num1} {oper} {num2} = {rez}")


def calculate(oper, num1, num2):
    """Функция для тестирования, возвращает результат операции"""
    if oper == "+":
        return num1 + num2
    elif oper == "-":
        return num1 - num2
    elif oper == "*":
        return num1 * num2
    elif oper == "/":
        if num2 == 0:
            raise ValueError("Деление на ноль")
        return num1 / num2
    elif oper == "^":
        return num1 ** num2
    elif oper == "%":
        return num1 % num2
    else:
        raise ValueError("Неверная операция")


if __name__ == "__main__":
    calculator()
