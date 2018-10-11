import math
import random as r

def fDistributionDensity(x):
    """
    Функция плотности распределения
    Аргументы:
    x - значение
    """
    a = 2*math.sqrt(3) + math.pi/6
    if 0 < x <= math.pi/6:
        return math.sin(x)
    elif math.pi/6 < x < a:
        return (x-a)/(math.pi/3 - 2*a)
    else:
        return 0

def continuousVariation(x):
    """
    Генерация непрерывной случайной величины по графику плотности

    """
    if x > math.pi / 6:
        print ("s2", fDistributionDensity(x))
    else:
        print ("s1", fDistributionDensity(x))

def our_rand():
    res = r.random()
    return (res, res * (2 * math.sqrt(3) + math.pi / 6))

N = 10 ** 2
ZN = []
for _ in range(N):
    (x_0_1, x) = our_rand()
    ZN.append((x_0_1, continuousVariation(x)))

n = 20
# промежутки
H = dict()
for i in range(n):
    H.update({i : 0})

# количество попаданий
for x, _ in ZN:
    ind = int(x * n)
    if ind == 20:
        ind -= 1
    H.update({ind : H.get(ind) + 1})

print(H)

# вывод графиков для H
import numpy as np
import matplotlib.pyplot as plt
data1 = list(H.values())
locs = np.arange(1, len(data1)+1)
width = 0.27
bar1 = plt.bar(locs, data1, width=width)
plt.xticks(locs + width*1.5, locs)
plt.show()