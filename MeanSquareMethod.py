import math
import time
#Метод средних квадратов
a =[]
a.append(0.2152)
for i in range(0,10):
    f=round( (round(a[i]**2,6))*100 - int((round(a[i]**2,6))*100),4)
    a.append(f)

print(a)
#Мультипликативный конгруэнтный метод
x = []
x.append(math.e)
x.append(math.pi)
for i in range(1,10**6):
    x.append((5*x[i-1] + x[i])%4)
print(x[8])
