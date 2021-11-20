import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import control.matlab as matlab
import colorama as color
import copy


def get_tf(inf, name):  # Эта функция нужна для получения передаточной функции
    num = inf.get(name)[0]
    den = inf.get(name)[1]
    return matlab.tf(num, den)


def step(tf):  # Функция строящая переходную характеристику
    print("Переходная характеристика:\n")
    print(tf)
    [y, x] = matlab.step(tf)
    plt.plot(x, y, "Blue")
    plt.title("Переходная характеристика")
    plt.xlabel("Time, sec")
    plt.ylabel("Value")
    plt.grid()
    plt.show()


def check_roots(tf):  # Функция проверяющая устойчивость системы по полюсам передаточной функции
    poles = matlab.pole(tf)  # Находим полюсы передаточной функции tf
    re_part = list(map(re, poles))  # Выделяется действительная часть
    im_part = list(map(im, poles))  # Выделяется мнимая часть
    plt.scatter(re_part, im_part)   # Строится точеный график
    plt.grid(True, which="minor")  # Включается промежуточные линии сеткци
    plt.grid(True, which="major")  # Влючается основные линии сеткци
    plt.title("Корни уравнения")   # Название графика
    plt.xlabel("Re")  # Подпись оси X
    plt.ylabel("Im")  # Подпись оси У
    plt.minorticks_on()
    plt.show()
    print("Полюсы: \n %s" % poles)
    stable = True  # Маркер устойчивости
    for pole in re_part:
        # Проходим по всех полюсам, если хотябы один имеет положительную дейсвтительную часть - система неустойчива
        if pole > 0:
            stable = False
            break
    if stable:
        print("Система устойчива")
    else:
        print("Система не устойчива. Среди полюсов есть полюсы с положительной дейсвительной частью")


def nyquist_graph():
    plt.title('Nyquist Diagram ')
    plt.ylabel('Imaginary Axis')
    plt.xlabel('Real Axis')
    matlab.nyquist(open_acs)
    plt.grid(True)
    plt.plot()
    plt.show()


def freq_check():
    mag, phase, omega = matlab.bode(open_acs, dB=False)
    plt.show()


def mikhailov():  # Построение годогрофа Михайлова
    a, p = symbols("a, p")  # Обозначем переменные a и p за символы соответсвенно a и p
    a_list = matlab.tfdata(close_acs)[1][0][0]  # Коэффициенты полинома знаметателя
    w = np.arange(0, 2.0, 0.05)  # Массив рассматриваемых частот
    expr = sum([a_list[i] * p ** (len(a_list) - i - 1) for i in range(len(a_list))])
    # Получение выражения характеристического полинома
    print("Уравнение: ", end="")
    print(expr)
    value = list(map(lambda x: expr.subs(p, complex(0, x)), w))  # Подставляем для вместо p --- jw для всех значений
    u, v = list(map(re, value)), list(map(im, value))  # Формируется действительная и мнимая части
    plt.plot(u, v) # Построение графика из двух полученных список
    plt.title("Годограф Михайлова")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.grid()
    plt.show()


def get_matrix_of_hurwitz(close):  # Функция для получения матрицы Гурвица
    a_list = matlab.tfdata(close)[1][0][0]  # Получаем массив коэффициентов характеристического полинома
    matrix = np.zeros((len(a_list) - 1, len(a_list) - 1), dtype="float64")  # Заполняем матрицу нулями
    k = 0
    i = 0
    while k <= (len(a_list) - 1):  # Цикл по массиву коэффициентов а. Получаем первые две строки матрицы
        if k == (len(a_list) - 1):
            matrix[1][i] = a_list[k]
            break
        else:
            matrix[1][i] = a_list[k]  # Записываем во вторую строку четные эелементы (0 - четный элемент)
            k += 1   # Переход к нечетному элементу
            matrix[0][i] = a_list[k]  # Записываем в первую строку нечетные элементы
            k += 1  # Переход к четному элементу
        i += 1  # Переход к следующему элементу массива
    for j in range(2, len(a_list) - 1):  # Заполнение остальных строк на основании первой и второй сторк
        if j % 2 == 0:  # Если строка четная, то используется певая строка иначе вторая
            matrix[j][j // 2:] += matrix[0][:len(a_list) - 1 - j // 2]
        else:
            matrix[j][j // 2:] += matrix[1][:len(a_list) - 1 - j // 2]
    return matrix


def hurwitz():  # Поиск критического Kос с помощью критерия Гурвица
    new_data = copy.deepcopy(data)
    # Производим глубокое копирование, чтобы при изменении данных не изменить их в исходном словаре
    step = 1  # Исходный шаг изменения Kос
    dev = 1  # Deviation - отклонение значения определителя от нуля (по сути значение определителя)
    while abs(dev) > 0.000001:  # Повторять поиск, пока значение отклонение больше заданного значения
        if dev < 0:
            # Если отклонение отрицательное, то система уже потеряла устойчивость, и значит
            # надо уменьшить шаг и повторить действия. При этом действие отменяется.
            new_data["ос"] = ([new_data['ос'][0][0] - step, 0], [1, 1])
            step = step / 2
        elif dev > 0:
            # Если отклонение положительное, то система устойчива, и значит можно повторять действия
            new_data["ос"] = ([new_data['ос'][0][0] + step, 0], [1, 1])
        # print(f"Текущее значение Kос = {new_data['ос'][0][0]}")
        # print(f"Текущее значение шага = {step}")
        w12 = get_tf(new_data, "ос")  # Пересчитваем передаточную функция для обратной связи
        open = w12 * w234  # Пересчитваем передаточную функцию для разомкнутой системы
        close = matlab.feedback(w234, w12)  # Пересчитваем передаточную функцию для замкнутной системы
        matrix = get_matrix_of_hurwitz(close)  # На основании новой передаточной функции определяем матрицу Гурвица
        dev = np.linalg.det(matrix[:len(matrix[0]) - 1, :len(matrix[0]) - 1])  # Рассчитываем значение определителя
        # print(f"Текущее значение определителя = {dev}")
    print(f"Текущее значение Kос = {new_data['ос'][0][0]}")
    return close, open


def acton():  # Функция для выполнения действий
    global close_acs, open_acs
    new_acs = ()
    is_continue = True  # Маркер проверяющий желание продолжнать выполнять те или иные действия
    while is_continue:
        act = input_digits("Что вы хотите сделать?\n"
                           "1 - Снять переходную характеристику системы\n"
                           "2 - Проверить устойчивость по корням\n"
                           "3 - Проверка по критерию Найквиста\n"
                           "4 - Определение запаса по устойчивости\n"
                           "5 - Построить годограф Михайлова\n"
                           "6 - Определение значения Kос при котором теряется устойчивость\n"
                           "7 - Повторить все действия для системы на границе устойчивости. "
                           "Для этого пунтка надо сначала сделать 6 пункт \n"
                           "8 - Завершить выполнение действий\n ")
        if act == 1:
            step(close_acs)
        elif act == 2:
            check_roots(close_acs)
        elif act == 3:
            nyquist_graph()
        elif act == 4:
            freq_check()
            print(open_acs)
        elif act == 5:
            mikhailov()
        elif act == 6:
            new_acs = hurwitz()
        elif act == 7:
            close_acs, open_acs = new_acs
        elif act == 8:
            is_continue = False
        else:
            print(color.Fore.RED + "Ведено число выходящее за диапазон! Попробуйте еще раз\n" + color.Style.RESET_ALL)


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


data = {"ос": ([0.2, 0], [1, 1]),
        "генератор": ([1], [10, 1]),
        "турбина": ([0.01, 1], [0.5, 1]),
        "иу": ([24], [4, 1])}
w1, w2, w3, w4 = get_tf(data, "ос"), get_tf(data, "генератор"), get_tf(data, "турбина"), get_tf(data, "иу")
w234 = w2 * w3 * w4
open_acs = w1 * w2 * w3 * w4
close_acs = matlab.feedback(w234, w1)
acton()
