import matplotlib.pyplot as plt
import control.matlab as matlab
import numpy
import math
import colorama as color


def inputDigit(maxDigit, text):  # Функция для проверки правильности ввода чисел
    newAttempt = True
    while newAttempt:
        inDigit = input(color.Fore.LIGHTCYAN_EX + text + color.Style.RESET_ALL)
        if inDigit.isdigit():
            outDigit = int(inDigit)
            if outDigit <= maxDigit:
                newAttempt = False
            else:
                print(color.Fore.RED + "Недопустимое числовое значение!" + color.Style.RESET_ALL)
        else:
            print(color.Fore.RED + "Введено не число!" + color.Style.RESET_ALL)
    return outDigit


def graph(title, y, x):
    figure1 = plt.figure(figsize=(7, 4))
    axes1 = figure1.add_subplot(1, 1, 1)
    axes1.plot(x, y)
    axes1.grid(True)
    axes1.set_title(title)
    axes1.set_xlabel('Время')
    axes1.set_ylabel('Амплитуда')


def action(link):
    timeLine = []
    for i in range(0, 10000):
        timeLine.append(i / 1000)
    [y, x] = matlab.step(link, timeLine)
    graph('Переходная характеристика', y, x)
    [y, x] = matlab.impulse(link, timeLine)
    graph("Импусльная характеристика", y, x)
    mag, phase, omega = matlab.freqresp(link, timeLine)
    graph("АЧХ", mag, timeLine)
    graph("ФЧХ", phase * 180 / math.pi, timeLine)
    plt.show()


class Link:
    def __init__(self):
        self.name = inputDigit(5, "Выберете звено:\n"
                               "1 - Безынерционное звено\n"
                               "2 - Апериодическое звено\n"
                               "3 - Интугрирующее звено\n"
                               "4 - Идеальное дифференцирующее звено\n"
                               "5 - Реальное дифференцирующее звено\n")
        if self.name == 1:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = 1
            self.tf = matlab.tf([self.k], [self.t])
        elif self.name == 2:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = inputDigit(10, "Введите T:\n")
            self.tf = matlab.tf([self.k], [self.t, 1])
        elif self.name == 3:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = 1
            self.tf = matlab.tf([self.k], [self.t, 0])
        elif self.name == 4:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = 1
            self.tf = matlab.tf([self.k, 0], [self.t])
        else:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = inputDigit(10, "Введите T:\n")
            self.tf = matlab.tf([self.k, 0], [self.t, 1])


link1 = Link()
tf = link1.tf
action(tf)
