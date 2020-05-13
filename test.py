from typing import List, Tuple


def euclidean_distance(point1, point2, price, money):
    return (((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5) * price - money


def replacement_loss(new, u, v, price, money):
    return euclidean_distance(u, new, price, money) + \
           euclidean_distance(v, new, price, money) - \
           euclidean_distance(u, v, price, money)


def solve_tsp_nearest_insertion(instance: List[Tuple[int, int]], price:int, money: List[int]):
    permutation = []
    not_used = set(range(len(instance)))

    begin, end = -1, -1
    min_distance = -1
    for v in range(1, len(instance)):
        new_distance = euclidean_distance(instance[0], instance[v], price, money[0])
        if new_distance < min_distance or min_distance == -1:
            begin = 0
            end = v
            min_distance = new_distance

    permutation.extend([begin, end])
    not_used.remove(begin)
    not_used.remove(end)

    for i in range(len(instance) - 2):
        new_vertex = -1
        min_distance = -1

        for u in not_used:
            vertex_distance = -1
            for v in permutation:
                new_distance = euclidean_distance(instance[u], instance[v], price, money[u])
                if new_distance < vertex_distance or vertex_distance == -1:
                    vertex_distance = new_distance
            if vertex_distance < min_distance or min_distance == -1:
                new_vertex = u
        not_used.remove(new_vertex)

        split_place = -1
        min_distance = -1
        for j in range(i + 2):
            new_distance = replacement_loss(instance[new_vertex], instance[permutation[j]],
                                            instance[permutation[(j + 1) % (i + 2)]], price, money[new_vertex])
            if new_distance < min_distance or min_distance == -1:
                split_place = j
                min_distance = new_distance

        permutation = permutation[0 : split_place + 1] + \
                      [new_vertex] + permutation[split_place + 1: i + 2]
    return permutation


class TspSolver:
    def __init__(self):
        pass


def read_dots():
    with open('Condition/data1.txt') as file:
        line = (file.readline()).split()
        n = int(line[0])
        price = int(line[1])
        k, M = int(line[2]), int(line[3])

        coordinates = [(0, 0)] * n
        money = [0] * n
        for i in range(n):
            line = file.readline()
            tokens = line.split()
            coordinates[i] = (int(tokens[0]), int(tokens[1]))
            money[i] = int(tokens[2])
    file.close()
    return n, price, k, M, coordinates, money


def reading_input():
    knapsack_volume = int(input())
    items_num = int(input())

    volume_list = []
    value_list = []
    for i in range(items_num):
        x, y = map(int, input().split())
        volume_list.append(x)
        value_list.append(y)


instance = read_dots()
n, price, k, M, instance, money = read_dots()
solution = solve_tsp_nearest_insertion(instance, price, money)
for i in range(len(solution)):
    solution[i] += 1
solution.append(1)
res = ' '.join(list(map(str, solution)))

print(res)
