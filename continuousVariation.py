import math
import random as r
import matplotlib.pyplot as plt

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

def continuousVariation():
    """
    Генерация непрерывной случайной величины по графику плотности

    """
    S1 = 1 - math.sqrt(3)/2
    S2 = math.sqrt(3)/2
    div = S1/S2
    ran = r.random()
    if ran > div:
        print ("s2", fDistributionDensity(ran))
    else:
        print ("s1", fDistributionDensity(ran))
    print(ran)

continuousVariation()
