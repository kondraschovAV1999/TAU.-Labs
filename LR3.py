import math
from sympy import *
import matplotlib.pyplot as plt
import control.matlab as matlab
import colorama as color
import numpy as np


def get_tf(inf, name):  # Эта функция нужна для получения передаточной функции
    num = inf.get(name)[0]
    den = inf.get(name)[1]
    return matlab.tf(num, den)


def graph(axes, title, y, x, color, xlabel, ylabel):  # Функция для построения отдельного графика
    axes.plot(x, y, color)  # Строится сам график уже внутри рабочей области
    axes.grid(True)  # Включение сетки
    axes.set_title(title)  # Наименование графика
    axes.set_xlabel(xlabel)  # Устанавливается подпись оси x
    axes.set_ylabel(ylabel)  # Устанавливается подпись оси у


def step(tf, numb_of_graphs):  # Функция строящая переходную характеристику
    figure = plt.figure(figsize=(16, 8))  # Создается объект класса Figure(по сути это холст, на которо мы рисуем)
    axes = figure.add_subplot(1, numb_of_graphs, 1)
    [y, x] = matlab.step(tf)
    y2 = np.empty(len(y))
    y3 = np.empty(len(y))
    y2.fill(0.95 * y[-1])
    y3.fill(1.05 * y[-1])
    graph(axes, "Переходная характеристика", y, x, "Blue", "Time, sec", "Value")
    axes.plot(x, y2, '--r', x, y3, '--r')
    return figure


def get_sigma(tf):  # Функция для получения перерегулирования
    [y, x] = matlab.step(tf)
    st_value = y[-1]
    max_value = np.amax(y)
    sigma = (max_value - st_value) / st_value * 100
    printf("Перерегулирование", sigma)
    return sigma


def get_tp(tf):  # Функция для получения времени регулирования
    [y, x] = matlab.step(tf)
    st_value = y[-1]
    for i in range(len(y) - 1, -1, -1):
        if abs(y[i] - st_value) >= 0.05 * st_value:
            printf("Время регулирования", x[i])
            return x[i]


def get_M(tf):
    timeLine = np.arange(0, 10, 0.001)
    mag, phase, omega = matlab.freqresp(tf, timeLine)
    max_value = np.amax(mag)
    start_value = mag[0]
    omega_s = timeLine[np.where(mag <= mag[0])[0][1]]
    tp = 4 * math.pi / omega_s
    # printf("Время регулирования", tp)
    printf("Показатель колебательности", max_value / start_value)
    return max_value / start_value, tp


def get_psi(tf, tp):
    [y, x] = matlab.step(tf)
    list_max = list()
    change_sing = False  # Флаг фиксирующий знак
    for i in range(2, len(y)):
        if y[i - 1] - y[i] < 0 and not change_sing:
            change_sing = True
        if y[i - 1] - y[i] > 0 and change_sing:
            change_sing = False
            list_max.append(y[i - 1])
    # print(list_max)
    if len(list_max) <= 1:
        print("Процесс апериодический")
        return 0, 0
    else:
        tk = float(x[np.where(y == list_max[1])[0]] - x[np.where(y == list_max[0])[0]])
        n = tp / tk
        return 1 - list_max[1] / list_max[0], n


def printf(text, var):
    print(text + " = {:.3f}".format(float(var)))


def choose_regulator(data):  # Функция для выбора исследуемого регулятора
    type_of_reg = input_digits("Выбор типа регулятора:\n"
                               "1 - П\n"
                               "2 - ПИД\n")
    if type_of_reg == 1:
        data['П'] = ([1], [1])
        data['И'] = ([0], [1])
        data['Д'] = ([0], [1])
    elif type_of_reg == 2:
        data['П'] = ([1], [1])
        data['И'] = ([1], [2, 0])
        data['Д'] = ([2.5, 0], [1])
    else:
        print(color.Fore.LIGHTCYAN_EX + "Ошибка ввода!" + color.Style.RESET_ALL)
        choose_regulator(data)
    return type_of_reg


def is_digit(string):  # Функция проверяющая строку является ли она числом или нет
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


def check_changes(data):  # Данная функция выполняет функцию обратной связи при подборе параметров регулятора
    w1 = get_tf(data, "П") + get_tf(data, "И") + get_tf(data, "Д")
    w2, w3, w4 = get_tf(data, "генератор"), get_tf(data, "турбина"), get_tf(data, "иу")
    w = w1 * w2 * w3 * w4
    close_acs = matlab.feedback(w, 1)
    print("Переходная характеристика:")
    print(close_acs)
    step(close_acs, 1)
    sigma = get_sigma(close_acs)
    tp = get_tp(close_acs)
    m, tp1 = get_M(close_acs)
    psi, n = get_psi(close_acs, tp)
    plt.show()
    return close_acs, sigma, tp, psi, n, tp1, m


def pick_param(data, type_of_reg, tf):  # Функция подбора параметров регулятора
    if type_of_reg == 1:
        act = input_digits("Выберете действие:\n"
                           "1 - Изменить параметр К \n"
                           "2 - Закончить подбор параметров\n")
    else:
        act = input_digits("Выберете действие:\n"
                           "1 - Изменить параметр К \n"
                           "2 - Изменить парметр Tи \n"
                           "3 - Изменить параметр Tд \n"
                           "4 - Закончить подбор параметров\n")
    if act == 1:
        data['П'][0][0] = input_digits("Введите значение K \n")
        return pick_param(data, type_of_reg, check_changes(data))
    elif act == 2:
        if type_of_reg == 1:
            return tf
        else:
            data['И'][1][0] = input_digits("Введите значение Tи \n")
            return pick_param(data, type_of_reg, check_changes(data))
    elif act == 3:
        if type_of_reg == 1:
            print(color.Fore.RED + "Число выходит за диапазон! " + color.Style.RESET_ALL)
            return pick_param(data, type_of_reg, check_changes(data))
        else:
            data['Д'][0][0] = input_digits("Введите значение Tд \n")
            return pick_param(data, type_of_reg, check_changes(data))
    elif act == 4:
        print(color.Fore.RED + "Число выходит за диапазон! " + color.Style.RESET_ALL)
        return pick_param(data, type_of_reg, check_changes(data))
    else:
        print(color.Fore.RED + "Число выходит за диапазон! " + color.Style.RESET_ALL)
        return pick_param(data, type_of_reg, check_changes(data))


def get_achx(tf, fig):
    axes = fig.add_subplot(1, 2, 2)  # Создаем рабочую область на который будут оси (изображаем на холсте)
    timeLine = np.arange(0, 10, 0.001)
    mag, phase, omega = matlab.freqresp(tf, timeLine)
    graph(axes, "АЧХ", mag, timeLine, "Blue", "w, рад/с", "Value")


def check_roots(tf):  # Функция проверяющая устойчивость системы по полюсам передаточной функции
    poles = matlab.pole(tf)  # Находим полюсы передаточной функции tf
    re_part = np.array(list(map(re, poles)))  # Выделяется действительная часть
    im_part = np.array(list(map(im, poles)))  # Выделяется мнимая часть
    a_min = np.amax(re_part)
    printf("Время регулирования", 3 / abs(a_min))
    template = im_part / re_part
    mu = np.amax(template)
    printf("Степерь колебательности", mu)
    printf("Перерегулирование", math.exp(-math.pi / mu) * 100)
    printf("Колебательность", (1 - math.exp(-2 * math.pi / mu)) * 100)


def integral(tf):
    [y, x] = matlab.step(tf)
    eps = y[-1] - y
    integr = 0
    for i in range(1, len(x)):
        integr += abs(eps[i] + eps[i - 1]) * (x[i] - x[i - 1]) / 2
    printf("Значение интеграла", integr)


def action():  # Функция выполнения действий
    data = {"генератор": ([1], [10, 1]),
            "турбина": ([0.01, 1], [0.5, 1]),
            "иу": ([24], [4, 1])}
    type_of_reg = choose_regulator(data)
    is_continue = True  # Маркер проверяющий желание продолжнать выполнять те или иные действия
    while is_continue:
        act = input_digits("Что вы хотите сделать?\n"
                           "1 - Подобрать параметры регуляторов\n"
                           "2 - Определить прямые оценки качества переходного процесса\n"
                           "3 - Определить косвенные оценки качества переходного процесса по корням\n"
                           "4 - Оценки качества по ЛАЧХ и ЛФЧХ \n"
                           "5 - Интегральная оценка\n"
                           "6 - Завершить выполнение действий\n ")
        if act == 1:
            tf, sigma, tp, psi, n, tp1, m = pick_param(data, type_of_reg, None)
        elif act == 2:
            try:
                printf("Перерегулирование", sigma)
                printf("Время регулирования", tp)
                printf("Степень затухания", psi)
                printf("Колебательность", n)
                fig = step(tf, 2)
                get_achx(tf, fig)
                plt.show()
            except UnboundLocalError:
                print(color.Fore.RED + "Предварительно требуется сделать 1-ый пункт!" + color.Style.RESET_ALL)
        elif act == 3:
            try:
                check_roots(tf)
            except UnboundLocalError:
                print(color.Fore.RED + "Предварительно требуется сделать 1-ый пункт!" + color.Style.RESET_ALL)
        elif act == 4:
            try:
                printf("Показатель колебательности", m)
                printf("Время регулирования", tp1)
                gm, pm, wg, wp = matlab.margin(tf)
                printf("Запас по амплитуде", gm)
                printf("Запас по фазе", pm)
                matlab.bode(tf)
                plt.show()
            except UnboundLocalError:
                print(color.Fore.RED + "Предварительно требуется сделать 1-ый пункт!" + color.Style.RESET_ALL)
        elif act == 5:
            integral(tf)
        elif act == 6:
            is_continue = False
        else:
            print(color.Fore.RED + "Ведено число выходящее за диапазон! Попробуйте еще раз\n" + color.Style.RESET_ALL)


action()
