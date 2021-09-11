import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import math
import colorama as color


def inputDigit(maxDigit, text):  # Функция для проверки правильности ввода чисел
    newAttempt = True
    while newAttempt:
        inDigit = input(text)
        if inDigit.isdigit():
            outDigit = int(inDigit)
            if outDigit <= maxDigit:
                newAttempt = False
            else:
                print("Недопустимое числовое значение!")
        else:
            print("Введено не число")
    return outDigit


def graph(num, title, y, x):
    pyplot.subplot(2, 1, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'purple')
    elif title == "Импусльная характеристика":
        pyplot.plot(x, y, 'green')
    pyplot.title(title)
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время ')


def checkLink(link):
    timeLine = []
    for i in range(0, 10000):
        timeLine.append(i / 1000)
    [y, x] = matlab.step(link, timeLine)
    graph(1, 'Переходная характеристика', y, x)
    [y, x] = matlab.impulse(link, timeLine)
    graph(2, "Импусльная характеристика", y, x)
    pyplot.show()


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


link1 = Link().tf
checkLink(link1)
