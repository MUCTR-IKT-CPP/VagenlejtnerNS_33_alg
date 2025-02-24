import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt


# Функция для минимизации
def objective_function(x):
    return x ** 2 + 10 - 10 * math.cos(2 * math.pi * x)


# Алгоритм отжига
def simulated_annealing(T0, Tmin, max_iter):
    # Начальная случайная точка
    x_current = random.uniform(-5, 5)
    F_current = objective_function(x_current)

    T = T0
    k = 1

    # Регистрируем время на каждой температуре
    times = []

    while T > Tmin and k <= max_iter:
        start_time = time.time()  # Начало замера времени

        # Генерация новой точки с учетом температуры
        x_new = x_current + T * np.random.standard_cauchy()  # заменили random на numpy
        F_new = objective_function(x_new)

        # Разница между значениями функции
        dF = F_new - F_current

        # Если dF < 0, принимаем новую точку
        if dF < 0 or random.random() < math.exp(-dF / T):
            x_current = x_new
            F_current = F_new

        # Охлаждаем температуру
        T = T0 / k
        k += 1

        # Окончание замера времени
        end_time = time.time()

        # Записываем время работы на каждом шаге
        times.append(end_time - start_time)

    return x_current, F_current, times


# Тестирование для разных Tmin
def test_minimum_temperature():
    Tmin_values = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    T0 = 1000
    max_iter = 10000
    times_results = []
    temperatures = []

    for Tmin in Tmin_values:
        _, _, times = simulated_annealing(T0, Tmin, max_iter)
        times_results.append(np.mean(times))  # усредненное время на каждом Tmin
        temperatures.append(1 / Tmin)  # инвертированная температура как ось X

    # Построение графика зависимости времени от инвертированной температуры
    plt.plot(temperatures, times_results, label="Average time vs 1/Tmin")
    plt.xlabel("1/Tmin (Inverted Temperature)")
    plt.ylabel("Average time (seconds)")
    plt.title("Simulated Annealing: Time vs Inverted Temperature")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    test_minimum_temperature()
