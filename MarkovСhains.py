import random as r
#марковская цепь (сумма вероятностей в строке равна 1)
chains = {1:[[1, 0.2], [2, 0.8]],
          2:[[3, 0.25], [4, 0.15], [5, 0.6]],
          3:[[3, 0.25], [5, 0.75]],
          4:[[1, 0.33], [4, 0.67]],
          5:[[6, 1]],
          6:[[1, 0.33], [4, 0.17], [7, 0.5]],
          7:[[8, 1]],
          8:[[5, 0.84], [8, 0.16]]}

#дважды стщхасттическая марковская цепь (сумма вероятностей в столбце и строке равна 1)
matrix = [[0.25, 0, 0.05, 0.1, 0.3, 0, 0.15, 0.15],
          [0.15, 0.25, 0, 0.05, 0.1, 0.3, 0, 0.15],
          [0.15, 0.15, 0.25, 0, 0.05, 0.1, 0.3, 0],
          [0, 0.15, 0.15, 0.25, 0, 0.05, 0.1, 0.3],
          [0.3, 0, 0.15, 0.15, 0.25, 0, 0.05, 0.1],
          [0.1, 0.3, 0, 0.15, 0.15, 0.25, 0, 0.05],
          [0.05, 0.1, 0.3, 0, 0.15, 0.15, 0.25, 0],
          [0, 0.05, 0.1, 0.3, 0, 0.15, 0.15, 0.25]
]

def dictToMatrix(chains):
    """преобразование словаря в матрицу"""
    matrix = []
    for state in range(1,len(chains)+1):
        if chains.get(state) is None:
            matrix.append([0 for i in len(chains)+1])
        else:
            tmp = []
            st = [x[0] for x in chains[state]]
            p = [x[1] for x in chains[state]]
            for i in range(1,len(chains)+1):
                if i in st:
                    tmp.append(p[st.index(i)])
                else:
                    tmp.append(0)
            matrix.append(tmp)
    return matrix


def matrixToDict(matrix):
    """преобразование матрицы в словарь"""
    dict = {}
    for state in range(len(matrix)):
        tmp = []
        for i in range(len(matrix)):
            if matrix[state][i] != 0:
                tmp.append([i+1,matrix[state][i]])
        dict[state+1] = tmp
    return dict

def verification(chains):
    """
    проверка цепи Маркова на соответсвие условию
    """
    for state in chains:
        if sum([x[1] for x in chains[state]])!= 1:
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
    превращенеие накопительной суммы возникновения событий в вероятности
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

    state = randProb(run, chains)
    while numOfMove >= 0:
        distribution = addDist(distribution, run, state)
        run = state
        state = randProb(run, chains)
        numOfMove-=1
    dist = probabilityLeveling(distribution)
    return dist

def printDict(distribution):
    for state in distribution:
        print("\nState:",state)
        for i in distribution[state]:
            print ("in",i[0],"p(",'%.3f'%i[1],")")
    print()

def printMatrix(distribution):
    for i in range(len(distribution)):
        print("\t",i+1,end='')
    print(end='\n\n')
    for i in range(len(distribution)):
        print(i+1,end="   ")
        for j in range(len(distribution)):
            if distribution[i][j] == 0:
                print("\t",0,end='')
            else:
                print("\t",'%.3f'%distribution[i][j],end='')
        print()
    print()

# dist=chainProbabilities(1, chains)
# printDict(dist)
# printMatrix(dictToMatrix(dist))
dict = matrixToDict(matrix)
printMatrix(matrix)
dist=chainProbabilities(1, dict)
printMatrix(dictToMatrix(dist))
