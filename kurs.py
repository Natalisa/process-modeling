numMemoryBlock = 4096
numCores = 1024
coreReserve = 20
tau = 1 #время появления задачи
# tFailure =

queue = []
memoryBlock = [1 for i in range(numMemoryBlock)]

cores = []
for i in range(numCores):
     if i < (numCores - coreReserve):
        cores.append(1)
     else:
        cores.append(2)
