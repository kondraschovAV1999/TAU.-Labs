import matplotlib.pyplot as plt
import control.matlab as matlab
import math
import colorama as color


def inputNumbers(maxNumber, text):  # Функция для проверки правильности ввода чисел
    # Параметры функции: maxNumber - предел по значению, вводимых чисел; text - текст выводимый на экран
    newAttempt = True  # Маркер, указывающий продолжение ввода
    while newAttempt:
        inDigit = input(color.Fore.LIGHTCYAN_EX + text + color.Style.RESET_ALL)
        if inDigit.isdigit():  # Проверка что введено число, если это так, то преобразуем строку в число
            outDigit = int(inDigit)
            if outDigit <= maxNumber:
                newAttempt = False
            else:
                print(color.Fore.RED + "Недопустимое числовое значение!" + color.Style.RESET_ALL)
        else:  # Если нет, то идет следующая попытка ввода
            print(color.Fore.RED + "Введено не число!" + color.Style.RESET_ALL)
    return outDigit


def getStep(tf, timeLine, color, step, label):  # Функция для получения переходной характеристики
    [y, x] = matlab.step(tf, timeLine)  # Получение переходной характеристики
    step.graph('Переходная характеристика', y, x, color, label)


def getImpulse(tf, timeLine, color, impulse, label):  # Функция для получения импульсной характеристики
    [y, x] = matlab.impulse(tf, timeLine)  # Получение импульсной характеристики
    impulse.graph("Импусльная характеристика", y, x, color, label)


def getFreq(tf, timeLine, color, achx, fchx, label):  # Функция для получения частотных характеристик
    mag, phase, omega = matlab.freqresp(tf, timeLine)  # Получение АЧХ, ФЧХ
    achx.graph("АЧХ", mag, timeLine, color, label)
    fchx.graph("ФЧХ", phase * 180 / math.pi, timeLine, color, label)


class Graph:  # Данный класс необходим для построения графиков
    # Класс нужен был для того, чтобы
    def __init__(self):
        figure = plt.figure(figsize=(7, 4))  # Создается объект класса Figure(по сути это холст, на которо мы рисуем)
        self.axes = figure.add_subplot(1, 1, 1)  # Создаем рабочую область на который будут оси (изображаем на холсте)

    def graph(self, title, y, x, color, label):  # Функция для построения отдельного графика
        self.axes.plot(x, y, color, label=label)  # Строится сам график уже внутри рабочей области
        self.axes.legend(loc="upper right")
        self.axes.grid(True)  # Включение сетки
        self.axes.set_title(title)  # Наименование графика
        self.axes.set_xlabel('Время')  # Устанавливается подпись оси x
        self.axes.set_ylabel('Амплитуда')  # Устанавливается подпись оси у


class Link:  # Создаем класс "Звено"
    def __init__(self):
        # Имеет четыре параметра name - тип звена, k и t характеризуют передаточную функцию
        #  а также tf - передаточная функция и changeTf - изменненая передаточная функция
        self.name = inputNumbers(5, "Выберете исследуемое звено:\n"
                                    "1 - Безынерционное звено\n"
                                    "2 - Апериодическое звено\n"
                                    "3 - Интугрирующее звено\n"
                                    "4 - Идеальное дифференцирующее звено\n"
                                    "5 - Реальное дифференцирующее звено\n")
        if self.name == 1:
            self.k = inputNumbers(10, "Введите k:\n")
            self.t = 1
            self.tf = matlab.tf([self.k], [self.t])
            self.changeTf = matlab.tf([2 * self.k], [self.t / 2])
        elif self.name == 2:
            self.k = inputNumbers(10, "Введите k:\n")
            self.t = inputNumbers(10, "Введите T:\n")
            self.tf = matlab.tf([self.k], [self.t, 1])
            self.changeTf = matlab.tf([2 * self.k], [self.t / 2, 1])
        elif self.name == 3:
            self.k = inputNumbers(10, "Введите k:\n")
            self.t = 1
            self.tf = matlab.tf([0, self.k], [self.t, 0])
            self.changeTf = matlab.tf([0, 2 * self.k], [self.t, 0])
        elif self.name == 4:
            self.k = inputNumbers(10, "Введите k:\n")
            self.t = 0.0000000000000001
            self.tf = matlab.tf([self.k, 0], [self.t, 1])
            self.changeTf = matlab.tf([2 * self.k, 0], [self.t, 1])
        else:
            self.k = inputNumbers(10, "Введите k:\n")
            self.t = inputNumbers(10, "Введите T:\n")
            self.tf = matlab.tf([self.k, 0], [self.t, 1])
            self.changeTf = matlab.tf([2 * self.k, 0], [self.t / 2, 1])

    def action(self):  # Данный метод отвечает за выполнение действий
        timeLine = []  # Список точек по времени
        for i in range(1, 10000):
            timeLine.append(i / 1000)
        wantToContinue = 1  # Флаг, отвечающий за продолжение построения графиков
        while wantToContinue == 1:
            motion = inputNumbers(3, "Что вы хотите сделать ?\n"
                                     "1 - Построить переходную характеристику\n"
                                     "2 - Построить импульсную характеристику\n"
                                     "3 - Построить частотные характеристики\n")
            if motion == 1:
                step = Graph()
                getStep(self.tf, timeLine, "black", step, "До")
                getStep(self.changeTf, timeLine, "blue", step, "После")
            elif motion == 2:
                impulse = Graph()
                getImpulse(self.tf, timeLine, "black", impulse, "До")
                getImpulse(self.changeTf, timeLine, "blue", impulse, "После")
            elif motion == 3:
                achx = Graph()
                fchx = Graph()
                getFreq(self.tf, timeLine, "black", achx, fchx, "До")
                getFreq(self.changeTf, timeLine, "blue", achx, fchx, "После")
            plt.show()
            wantToContinue = inputNumbers(1, "Хотите продолжить ? \n"
                                             "1 - Да\n"
                                             "0 - Нет\n")


link1 = Link()  # Создается объект класса Link
tf = link1.tf  # Получаем передаточную функцию
tf1 = link1.changeTf  # Получаем передаточную функцию измененную
print(color.Fore.LIGHTCYAN_EX + "Передаточные функции:" + color.Style.RESET_ALL)
print(tf)
print(tf1)
link1.action()  # Построение всех графиков
