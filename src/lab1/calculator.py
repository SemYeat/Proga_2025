def calculator():
    print("Операции")
    print("+")
    print("-")
    print("*")
    print("/")
    print("^")
    print("%")

    while True:
        oper = int(input())
        if oper not in ["+", "-", "*", "/", "^", "%"]:
            print("Неверная операция")
            continue
        try:
            num1 = float(input("Введи первое число:"))
            num2 = float(input("Введи второе число"))
        except ValueError:
            print("Не верно. Введите числа")
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
            rezz = num1**num2
        elif oper == "%":
            rez = num1 % num2

        print(f" {num1} {oper} {num2} = {rez}")


if __name__ == "__main__":
    calculator()git checkout master
