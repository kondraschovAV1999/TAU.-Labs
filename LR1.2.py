import matplotlib.pyplot as plt
import control.matlab as matlab
import numpy
import math
import colorama as color


def inputDigit(maxDigit, text):  # Функция для проверки правильности ввода чисел
    # Параметры функции: maxDigit - предел по значению, вводимых чисел; text - текст выводимый на экран
    newAttempt = True  # Маркер, указывающий продолжение ввода
    while newAttempt:
        inDigit = input(color.Fore.LIGHTCYAN_EX + text + color.Style.RESET_ALL)
        if inDigit.isdigit():  # Проверка что введено число, если это так, то преобразуем строку в число
            outDigit = int(inDigit)
            if outDigit <= maxDigit:
                newAttempt = False
            else:
                print(color.Fore.RED + "Недопустимое числовое значение!" + color.Style.RESET_ALL)
        else:  # Если нет, то идет следующая попытка ввода
            print(color.Fore.RED + "Введено не число!" + color.Style.RESET_ALL)
    return outDigit


def graph(title, y, x):  # Функция для построения отдельного графика
    figure1 = plt.figure(figsize=(7, 4))   # Создается объект класса Figure(по сути это холст, на котороым рисуем)
    axes1 = figure1.add_subplot(1, 1, 1)  # Создаем рабочую область на который будут оси (изображаем на холсте)
    axes1.plot(x, y, "black")  # Строится сам график уже внутри рабочей области
    axes1.grid(True)  # Включение сетки
    axes1.set_title(title)  # Наименование графика
    axes1.set_xlabel('Время')   # Устанавливается подпись оси x
    axes1.set_ylabel('Амплитуда')  # Устанавливается подпись оси у


def action(link):  # Функция для построения всех графиков
    timeLine = []  # Список точек по времени
    for i in range(1, 10000):
        timeLine.append(i / 1000)
    [y, x] = matlab.step(link, timeLine)  # Получение переходной характеристики
    graph('Переходная характеристика', y, x)
    [y, x] = matlab.impulse(link, timeLine)
    graph("Импусльная характеристика", y, x)  # Получение импульсной характеристики
    mag, phase, omega = matlab.freqresp(link, timeLine)  # Получение АЧХ, ФЧХ
    graph("АЧХ", mag, timeLine)
    graph("ФЧХ", phase * 180 / math.pi, timeLine)
    plt.show()


class Link:  # Создаем класс "Звено"
    def __init__(self):
        # Имеет четыре параметра name - тип звена, k и t характеризуют передаточную функцию и tf - передаточная функция
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
            self.tf = matlab.tf([0, self.k], [self.t, 0])
        elif self.name == 4:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = 0.00000000001
            self.tf = matlab.tf([self.k, 0], [self.t, 1])
        else:
            self.k = inputDigit(10, "Введите k:\n")
            self.t = inputDigit(10, "Введите T:\n")
            self.tf = matlab.tf([self.k, 0], [self.t, 1])


link1 = Link()  # Создается объект класса Link
tf = link1.tf  # Получаем передаточную функцию
print(color.Fore.LIGHTCYAN_EX + "Передаточная функция:" + color.Style.RESET_ALL)
print(tf)
action(tf)  # Построение всех графиков
