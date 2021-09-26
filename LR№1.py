import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import math
import colorama as color


def choice():  # Отвечает за выбор звена
    inertialessUnitName = "Безынерционное звено"
    aperiodicUnitName = "Апериодическое звено"
    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input("Введите номер команды:\n"
                          "1 -" + inertialessUnitName + ";\n"
                                                        "2 -" + aperiodicUnitName + ".\n")
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = "Безынерционное звено"
            elif userInput == 2:
                name = "Апериодическое звено"
            else:
                print(color.Fore.RED + 'Недопустимое числовое значение!\n')
                needNewChoice = True

        else:
            print(color.Fore.RED + 'Пожалуйства, введите числовое значение!\n')
            needNewChoice = True
    return name


def getUnit(name):  # Мат.описание звена по его имени
    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        needNewChoice = False
        k = input('Пожалуйста, введите коэффииент "k": ')
        t = input('Пожалуйста, введите коэффииент "k": ')
        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            if name == "Безынерционное звено":
                unit = matlab.tf([k], [1])
            elif name == "Апериодическое звено":
                unit = matlab.tf([k], [t, 1])
        else:
            print(color.Fore.RED + 'Пожалуйства, введите числовое значение!\n')
            needNewChoice = True
    return unit


def graph(num, title, y, x):
    pyplot.subplot(2, 1, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'purple')
    elif title == "Импусльная характеристика":
        pyplot.plot(x, y, 'green')
    pyplot.title(title)
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время (с)')


unitName = choice()
unit = getUnit(unitName)
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 1000)

[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная характеристика', y, x)
[y, x] = matlab.impulse(unit, timeLine)
graph(2, "Импусльная характеристика", y, x)
pyplot.show()
