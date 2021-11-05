import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import control.matlab as matlab
import colorama as color
import linecache as line


def get_tf(number_of_line):
    num = list(map(float, line.getline("input", number_of_line).strip().split(" ")))
    number_of_line += 1
    den = list(map(float, line.getline("input", number_of_line).strip().split(" ")))
    return matlab.tf(num, den)


def step(tf):
    time = []  # Список точек по времени
    for i in range(1, 100000):
        time.append(i / 1000)
    [y, x] = matlab.step(tf, time)
    plt.plot(x, y, "Blue")
    plt.title("Переходная характеристика")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid()
    plt.show()


def check_roots(tf):
    roots = matlab.pole(tf)
    print("Полюса: \n %s" % roots)
    stable = True
    for root in roots:
        if re(root) >= 0:
            is_stable = False
            break
    if stable:
        print("Система устойчива")
    else:
        print("Система не устойчива. Среди корней есть корни с положительной дейсвительной частью")


def acton(tf):
    is_continue = True
    while is_continue:
        act = input_digits("Что вы хотите сделать?\n"
                           "1 - Снять переходную характеристику системы\n"
                           "2 - Проверить устойчивость по корням\n"
                           "3 - Завершить выполнение действий\n")
        if act == 1:
            step(tf)
        elif act == 2:
            check_roots(tf)
        elif act == 3:
            is_continue = False
        else:
            print("Ведено число выходящее за диапазон! Попробуйте еще раз\n")


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def input_digits(text):  # Функция для проверки правильности ввода чисел
    newAttempt = True  # Маркер, указывающий продолжение ввода
    while newAttempt:
        in_digit = input(color.Fore.LIGHTCYAN_EX + text + color.Style.RESET_ALL)
        if is_digit(in_digit):  # Проверка что введено число, если это так, то преобразуем строку в число
            out_digit = float(in_digit)
            newAttempt = False
        else:  # Если нет, то идет следующая попытка ввода
            print(color.Fore.RED + "Введено не число!" + color.Style.RESET_ALL)
    return out_digit


w1 = get_tf(1)
w2 = get_tf(3)
w3 = get_tf(5)
w4 = get_tf(7)
w234 = w2 + w3 + w4
w = matlab.feedback(w234, w1)
acton(w)
