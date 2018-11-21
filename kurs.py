import random
import time
from threading import Thread
numMemoryBlock = 4096
numCores = 1024
coreReserve = 20
tau = 1 #время появления задачи
# tFailure =

queue = []
memoryBlock = [1 for i in range(numMemoryBlock)]


class Tasks(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(tau)
            ter = 0.05
            v = random.randint(1, 100)
            n = random.randint(4, 256)
            queue.append((ter, v, n))
            print(queue)

class Work(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global numMemoryBlock
        global numCores
        global coreReserve
        while True:
            if queue != []:
                (ter, v, n) = queue.pop(0)
                failure = random.randint(0, 1000)
                numCores -= failure
                if coreReserve >= failure:
                    if coreReserve <= 0:
                        print("Нет доступных ядер")
                        exit(-1)
                    numCores += coreReserve - failure
                else:
                    if coreReserve <= 0:
                        print("Нет доступных ядер")
                        exit(-1)
                    numCores += failure
                coreReserve -= failure
                if numCores <= 0:
                    print("Нет доступных ядер")
                    exit(-1)

                numMemoryBlock -= v
                numCores -= n
                time.sleep(ter)
                numMemoryBlock += v
                numCores += n
                print(numMemoryBlock, numCores)


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

    time.sleep(1000)
