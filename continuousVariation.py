import math
import random as r

def continuousVariation(ep1):
    """
    Генерация непрерывной случайной величины по графику плотности

    """
    if ep1 < (1 - math.sqrt(3) / 2):
        x = math.acos(1 - (2 - math.sqrt(3))/2 * r.random())
    else:
        x = 2 * math.sqrt(3) +  math.pi / 6 - 2 * math.sqrt(3) * r.random()
    return x

def our_rand():
    res = r.random()
    return (res, continuousVariation(res))

N = 10 ** 4
ZN = []
for _ in range(N):
    (x_0_1, x) = our_rand()
    ZN.append((x_0_1, continuousVariation(x)))

n = 50
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
