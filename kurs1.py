import random
import time
import pprint

queue = []

# начальные данные
NUM_MEMORY_BLOCK = 4096
NUM_CORES = 1024
CORE_RESERVE = 20
FAILURE_PERSENT = 0.3

memory_blocks = []
cores = []
cores_reserve = []

calendar = []


# создание задачи
def get_task():
    ter = random.randint(1, 10) # время выполнения
    v = random.randint(1, 100) # память
    n = random.randint(4, 256) # ядра
    return ter, v, n


# работа с памятью
# занятие памяти
def get_memory_blocks(num):
    flag = False
    position = 0
    for n, _ in enumerate(memory_blocks):
        sum = 0
        for j in range(num):
            sum += memory_blocks[n + j]
        if sum == 0:
            for j in range(num):
                memory_blocks[n + j] = 1
            flag = True
            position = n
            break
    return flag, position, num


# освобождение памяти
def clean_memory_blocks(position, num):
    for i in range(num):
        memory_blocks[position + i] = 0


# работа с ядрами
# занятие памяти
def get_cores(num):
    flag = False
    position = 0
    for n, _ in enumerate(cores):
        sum = 0
        for j in range(num):
            if n + j < len(cores):
                sum += cores[n + j]
            else:
                return flag, position, num
        if sum == 0:
            for j in range(num):
                cores[n + j] = 1
            flag = True
            position = n
            break
    return flag, position, num


# освобождение памяти
def clean_cores(position, num):
    for i in range(num):
        cores[position + i] = 0


# выход из строя
def failure_cores():
    fail = random.random()
    if fail <= FAILURE_PERSENT:
        fail_count = -1
        if NUM_CORES * fail >= 1:
            fail_count = random.randint(1, int(NUM_CORES * fail))
        fail_position = random.randint(0, NUM_CORES)
        return True, fail_count, fail_position
    else:
        return False, -1, -1


def failure_memory():
    fail = random.random()
    if fail <= FAILURE_PERSENT:
        fail_count = -1
        if NUM_MEMORY_BLOCK * fail >= 1:
            fail_count = random.randint(1, int(NUM_MEMORY_BLOCK * fail))
        fail_position = random.randint(0, NUM_MEMORY_BLOCK)
        return True, fail_count, fail_position
    return False, -1, -1


# убийство ресурсов
def drop_cores(position, num):
    for i in range(num):
        if position + i < len(cores):
            cores[position + i] = 999
        else:
            print("Закончились ядра")
            exit(-1)


def drop_memory(position, num):
    for i in range(num):
        if position + i < len(memory_blocks):
            memory_blocks[position + i] = 999
        else:
            print("Закончились блоки памяти")
            exit(-1)

if __name__ == "__main__":
    # начальные 2 задачи
    queue.append(get_task())
    queue.append(get_task())

    # заполнение начальных массивов
    for _ in range(NUM_CORES):
        cores.append(0)
    for _ in range(NUM_MEMORY_BLOCK):
        memory_blocks.append(0)
    for _ in range(CORE_RESERVE):
        cores_reserve.append(0)

    pos = 0
    time_machine = 0
    while True:
        if not queue:
            break
        # получение задачи
        ter, v, n = queue.pop(0)

        # отработка задачи
        flag_cores, position_cores, _ = get_cores(n)
        if not flag_cores:
            print("Нет доступных ядер")
            break
        flag_memory, position_memory, _ = get_memory_blocks(v)
        if not flag_memory:
            print("Нет доступной памяти")
            break
        calendar.append((time_machine, position_cores, n, position_memory, v))
        time_machine += ter
        clean_cores(position_cores, n)
        clean_memory_blocks(position_memory, v)

        # выход из строя
        fail_core_flag, fail_core_count, fail_core_position = failure_cores()
        fail_memory_flag, fail_memory_count, fail_memory_position = failure_memory()
        if fail_core_flag:
            drop_cores(fail_core_position, fail_core_count)
        if fail_memory_flag:
            drop_memory(fail_memory_position, fail_memory_count)

        queue.append(get_task())
        pos += 1
        pprint.pprint(calendar)
        time.sleep(1)

    print(calendar)