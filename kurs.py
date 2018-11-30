import random
import time
from threading import Thread
import threading
from tkinter import *

root = Tk()
#-----------Исходные данные------------------------------------

NUM_MEMORY_BLOCK = 4096
NUM_CORES = 1024
CORE_RESERVE = 20
TAU = 1 #время появления задачи

#-----------Общие ресурсы в системе------------------------------------
numMemoryBlock = NUM_MEMORY_BLOCK
numCores = NUM_CORES
coreReserve = CORE_RESERVE

mutex = threading.Lock()
mutexNum = threading.Lock()
mutexReserve = threading.Lock()

num = [i for i in range(1000)] #номер задачи
queue = []
memoryBlock = [1 for i in range(numMemoryBlock)]

#-----------ИНТЕРФЕЙС-----------------------------------------------------

MainPanel = LabelFrame (root, text="Характеристики системы")
lbNumCores = Label(MainPanel,text="Количество ядер")
eNumCores = Entry(MainPanel,width=50)
lbNumCores.pack(side=LEFT)
eNumCores.pack(side=LEFT)
lbCoreReserve = Label(MainPanel,text="Количество ядер(резерв)")
eCoreReserve = Entry(MainPanel,width=50)
lbCoreReserve.pack(side=LEFT)
eCoreReserve.pack(side=LEFT)
lbNumMemoryBlock = Label(MainPanel,text="Количество блоков памяти")
eNumMemoryBlock = Entry(MainPanel,width=50)
lbNumMemoryBlock.pack(side=LEFT)
eNumMemoryBlock.pack(side=LEFT)
MainPanel.pack()

failureAndRecovery = LabelFrame (root, text="Выход из строя и востановление")
tFailureAndRecovery = Text(failureAndRecovery)
tFailureAndRecovery.pack()
failureAndRecovery.pack(side=LEFT)

taskManager = LabelFrame (root, text="Менеджер задач")
eTaskManagerStart = Text(taskManager, width=40)
eTaskManagerStart.pack(side=LEFT)
eTaskManagerCompleted = Text(taskManager, width=40)
eTaskManagerCompleted.pack()
taskManager.pack()

#-------------------------------------------------------------------------
class Tasks(Thread):
    """
    Генерирует задачи раз в TAU секунд
    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(TAU)
            mutexNum.acquire()
            Num = num.pop(0)
            mutexNum.release()
            #ter = 0.05
            ter = random.randint(1, 10)
            v = random.randint(1, 100)
            n = random.randint(4, 256)
            queue.append((Num, ter, v, n))
            print(queue)

class Task(Thread):
    """
    Поток выполнения одной задачи
    """
    global numCores
    global numMemoryBlock
    global coreReserve
    global num

    def __init__(self, Num, ter, v, n):
        self.ter = ter
        self.v = v
        self.n = n
        self.Num = Num
        Thread.__init__(self)

    def run(self):
        global numCores
        global numMemoryBlock
        global coreReserve

        s = " Start task №"+ str(self.Num) +"\t t=" + str(self.ter) + "\t MB=" \
        + str(self.v) + "\t C=" +str(self.n) +"\t\n"
        eTaskManagerStart.insert(1.0,s)
        #print((self.ter, self.v, self.n),"start")
        while True:
            if (numMemoryBlock > self.v and numCores > self.n):
                mutex.acquire()
                numMemoryBlock -= self.v
                numCores -= self.n
                mutex.release()

                time.sleep(self.ter)

                mutex.acquire()
                numMemoryBlock += self.v
                numCores += self.n
                mutex.release()
                #print((self.ter, self.v, self.n),"completed")
                s = "Сompleted task №"+ str(self.Num) +"\t t=" + str(self.ter) + \
                "\t MB="  + str(self.v) + "\t C=" +str(self.n) +"\t\n"
                eTaskManagerCompleted.insert(1.0,s)

                mutexNum.acquire()
                num.append(self.Num)
                num.sort()
                mutexNum.release()
                break
            else:
                time.sleep(TAU)

class Failure(Thread):
    """
    Поток выполнения выхода из строя
    """
    global numCores
    global numMemoryBlock
    global coreReserve

    def __init__(self):
        Thread.__init__(self)

    def recover(self):
        global numCores
        global numMemoryBlock
        global coreReserve
        while True:
            if coreReserve >= self.failure:
                mutexReserve.acquire()
                coreReserve -= self.failure
                mutexReserve.release()

                mutex.acquire()
                numCores += coreReserve - self.failure
                mutex.release()
                break
            else:
                 if coreReserve <= 0:
                    time.sleep(TAU)

    def funFailure(self):
        global numCores
        global numMemoryBlock
        global coreReserve
        self.failure = random.randint(0, 10)#сколько выходит из строя?

        mutex.acquire()
        numCores -= self.failure
        if numCores < 0:
            numCores = 0
        mutex.release()

        #print("failure cores",self.failure)
        s = "failure cores "+ str(self.failure) + "\n"
        tFailureAndRecovery.insert(1.0,s)
        self.recover()

    def run(self):
        while True:
            time.sleep(TAU)
            self.funFailure()

class Work(Thread):
    """
    Берет задачу на выполнение
    """
    def __init__(self):
        Thread.__init__(self)

    def monitoring(self):
        """
        Вывод текущих характеристик системы в интерфейс
        """
        global numMemoryBlock
        global numCores
        global coreReserve
        eNumCores.delete(0,END)
        eNumCores.insert(0, numCores)
        eNumMemoryBlock.delete(0,END)
        eNumMemoryBlock.insert(0, numMemoryBlock)
        eCoreReserve.delete(0,END)
        eCoreReserve.insert(0, coreReserve)
        #print("numMemoryBlock ",numMemoryBlock, "numCores ", numCores)

    def run(self):
        while True:
            if queue != []:
                self.monitoring()
                queue.sort()
                (Num, ter, v, n) = queue.pop(0)
                task = Task(Num, ter, v, n)
                task.start()

class Recover(Thread):
    """
    Востанавливает вышедших из строя ядер
    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global coreReserve
        while True:
            time.sleep(TAU)
            if coreReserve < CORE_RESERVE:
                resv = random.randint(0, 10)

                mutexReserve.acquire()
                coreReserve += resv #сколько надо востанавливать?
                if coreReserve > CORE_RESERVE:
                    raz = resv - (coreReserve - CORE_RESERVE)
                    coreReserve = CORE_RESERVE
                    s = "resover core "+ str(raz) + "\n"
                    tFailureAndRecovery.insert(1.0,s)
                mutexReserve.release()

                #print("resover core ", coreReserve)

if __name__ == "__main__":
    cores = []
    for i in range(numCores):
         if i < (numCores - coreReserve):
            cores.append(1)
         else:
            cores.append(2)

    tasks = Tasks()
    tasks.start()

    work = Work()
    work.start()

    failure = Failure()
    failure.start()

    recover = Recover()
    recover.start()

    root.mainloop()

    time.sleep(1000)
