import random
import time
import pprint
import math

queue = []
queue_finish = []

# начальные данные
NUM_MEMORY_BLOCK = 4096
NUM_CORES = 1024
CORE_RESERVE = 20
FAILURE_PERSENT = 0.4

memory_blocks = []
cores = []
cores_reserve = []

calendar = []
calendar_otkaz = []
calendar_otkaz_voss = []

num_task = 0

otkaz = {}


# создание задачи
def get_task():
    global num_task
    ter = random.randint(1, 10)  # время выполнения
    v = random.randint(1, 100)  # память
    n = random.randint(4, 256)  # ядра
    num_task += 1
    return ter, v, n, num_task


# работа с памятью
# занятие памяти
def get_memory_blocks(num):
    flag = False
    position = 0
    for n, _ in enumerate(memory_blocks):
        sum = 0
        for j in range(num):
            if n + j < len(memory_blocks):
                sum += memory_blocks[n + j]
            else:
                sum = 999
                break
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
            # else:
            #     return flag, position, num
        if sum == 0:
            for j in range(num):
                if n + j < len(cores):
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
        # print(fail_count)
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


# восстановление ядер
def restore_cores(num):
    for n, i in enumerate(cores):
        if i == 999:
            if num > 0:
                num -= 1
            cores[n] = 0


# восстановление памяти
def restore_memory(num):
    for n, i in enumerate(memory_blocks):
        if i == 999:
            if num > 0:
                num -= 1
            memory_blocks[n] = 0


# убийство ресурсов
def drop_cores(position, num):
    for i in range(num):
        if position + i < len(cores):
            cores[position + i] = 999


def drop_memory(position, num):
    for i in range(num):
        if position + i < len(memory_blocks):
            memory_blocks[position + i] = 999


def sr_time(lst):
    sum = 0
    for _, start, finish in lst:
        sum += finish - start
    if len(lst) > 0:
        return sum / len(calendar)
    else:
        return 0

if __name__ == "__main__":
    # начальные 1000 задач
    # for i in range(1000):
    #     queue.append(get_task())
    #     otkaz[i] = 0

    # заполнение начальных массивов
    for _ in range(NUM_CORES):
        cores.append(0)
    for _ in range(NUM_MEMORY_BLOCK):
        memory_blocks.append(0)
    for _ in range(CORE_RESERVE):
        cores_reserve.append(0)

    pos = 0
    time_machine = 0
    queue.append(get_task())
    while pos < 1000:
        if not queue:
            break
        # получение задач
        ter, v, n, num_task = queue.pop(0)

        time_machine += round(-math.log(random.random(), math.e), 3)

        queue.append(get_task())

        # print(calendar_otkaz_voss)
        if random.random() < 0.1:
            restore_cores(random.randint(0, NUM_CORES))
        print(sr_time(calendar_otkaz_voss))

        # отработка задачи
        flag_cores, position_cores, _ = get_cores(n)
        if not flag_cores:
            if (num_task, time_machine) not in calendar_otkaz:
                calendar_otkaz.append((num_task, time_machine))
            queue.append((ter, v, n, num_task))
            continue
        else:
            for el, time_ in calendar_otkaz:
                if el == num_task:
                    calendar_otkaz_voss.append((num_task, time_, time_machine))
                    calendar_otkaz.remove((el, time_))
                    break

        flag_memory, position_memory, _ = get_memory_blocks(v)
        if not flag_memory:
            print("Нет доступной памяти")
            if (num_task, time_machine) not in calendar_otkaz:
                calendar_otkaz.append((num_task, time_machine))
            queue.append((ter, v, n, num_task))
        else:
            for el, time_ in calendar_otkaz:
                if el == num_task:
                    calendar_otkaz_voss.append((num_task, time_, time_machine))
                    calendar_otkaz.remove((el, time_))
                    break
        calendar.append((time_machine, 'счет', time_machine + ter, n, position_cores, v, position_memory))
        queue_finish.append((time_machine + ter, n, position_cores, v, position_memory))

        time_for_finish, _, _, _, _ = queue_finish[0]
        if time_for_finish == time_machine:
            _, cores_count, position_cores, memory, position_memory = queue_finish.pop(0)
            clean_cores(position_cores, cores_count)
            clean_memory_blocks(position_memory, memory)

        # выход из строя
        fail_core_flag, fail_core_count, fail_core_position = failure_cores()
        # fail_memory_flag, fail_memory_count, fail_memory_position = failure_memory()
        if fail_core_flag:
            result = drop_cores(fail_core_position, fail_core_count)
            if result == -1:
                break
            else:
                calendar.append((time_machine, 'выход из строя', fail_core_position, fail_core_count))
                calendar.append(
                    (time_machine + random.randint(0, 10), 'восстановление', fail_core_position, fail_core_count))
        # if fail_memory_flag:
        #     if drop_memory(fail_memory_position, fail_memory_count) == -1:
        #         break

        # queue.append(get_task())
        pos += 1
        calendar.sort()
        # pprint.pprint(calendar)
        # pprint.pprint(otkaz)
        # pprint.pprint(calendar_otkaz)
        # pprint.pprint(calendar_otkaz_voss)
        # time.sleep(1)

    pprint.pprint(calendar)
    print(len(calendar))
    # pprint.pprint(otkaz)
