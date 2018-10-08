import random as r
chains = {1:[(1, 0.2), (2, 0.8)],
          2:[(3, 0.25), (4, 0.15), (5, 0.6)],
          3:[(3, 0.25), (5, 0.75)],
          4:[(1, 0.33), (4, 0.67)],
          5:[(6, 1)],
          6:[(1, 0.33), (4, 0.17), (7, 0.5)],
          7:[(8, 1)],
          8:[(5, 0.84), (8, 0.16)]}

def verification(chains):
    """
    проверка цепи Маркова на соответсвие условию
    """
    for state in range(1, len(chains)+1):
        if sum([x[1] for x in chains[state]]) != 1:
            return False
    return True

def randProb(state, chains):
    """
    выбор куда перейти
    state - состояние
    chains - матрица состояний в цепях Маркова
    """
    rand = r.random()
    states = chains[state]
    mass = [x[1] for x in states]
    sum = 0
    count = 0
    while True:
        if sum < rand:
            sum += mass[count]
            count += 1
        else:
            return states[count-1][0]

def addDist(distribution, run, state):
    """
    корректировка матрицы распределения
    distribution - матрица
    run - состояние из которого пришли
    state - состояние в которое перешли
    """
    #если из такого состояния еще не было
    if distribution.get(run) is None:
        distribution[run] = [[state, 1]]
        return distribution
    else:
        y = [x for x in distribution.get(run) if x[0] == state]
        #если в такое состояние еще не переходили
        if y == []:
            tmp = distribution.get(run)
            tmp.append([state,1])
            distribution[run] = tmp
            return distribution

        tmp = []
        for i in distribution.get(run):
            if i[0] == state:
                tmp.append([state, i[1]+1])
            else:
                tmp.append(i)
        distribution[run] = tmp
    return distribution

def probabilityLeveling(distribution):
    """
    превращенеие сумм возникновения событий в вероятности
    """
    for state in distribution:
        s = sum([x[1] for x in distribution.get(state)])
        tmp = []
        for i in distribution.get(state):
            tmp.append([i[0],i[1]/s])
        distribution[state] = tmp
    return (distribution)

def chainProbabilities(run, chains, numOfMove = 10**4, distribution = {}):
    """
    подсчет распределения вероятностей в перемещении по матрице
    run - начальное состояние
    chains - матрица состояний в цепях Маркова
    distribution - распределение вероятностей в процессе работы функции
    numOfMove - необходиоме количество шагов
    """
    #рекурсия не позволяет в глубь больше 100
    # if numOfMove != 0:
    #     state = randProb(run, chains)
    #     #print("\nis",run,"in",state)
    #     dist = addDist(distribution, run, state)
    #     #print(distribution)
    #     return chainProbabilities(state, chains, numOfMove-1, dist)
    # else:
    #     dist = probabilityLeveling(distribution)
    #     return dist

    state = randProb(run, chains)
    while numOfMove >= 0:
        distribution = addDist(distribution, run, state)
        run = state
        state = randProb(run, chains)
        numOfMove-=1
    dist = probabilityLeveling(distribution)
    return dist

def printMatrix(distribution):
    for state in distribution:
        print("\nState:",state)
        for i in distribution[state]:
            print ("in",i[0],"p(",'%.3f'%i[1],")")


dist=chainProbabilities(1, chains)
#print(dist)
printMatrix(dist)
