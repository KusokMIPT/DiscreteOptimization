from typing import List, Tuple

from tqdm import tqdm


def read_input():
    with open('data/data2.txt') as file:
        line = (file.readline())

        n, price, k, M = map(int, line.split())

        coordinates = [(0, 0)] * n
        money = [0] * n

        for i in range(n):
            line = file.readline().split()
            coordinates[i] = (int(line[0]), int(line[1]))
            money[i] = int(line[2])
    return n, price, k, M, coordinates, money


class CaptainMiptSolver():
    def __init__(self):
        self.price = price

    def solve(self, price):
        pass


def euclidean_distance(point1, point2, price, money):
    return (((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5) * price - money


def replacement_loss(new, u, v, price, money):
    return euclidean_distance(u, new, price, money) + \
           euclidean_distance(v, new, price, money) - \
           euclidean_distance(u, v, price, money)


def solve_tsp_nearest_insertion(coordinates: List[Tuple[int, int]], price: int, money_list: List[int]):
    permutation = []
    not_used = set(range(len(coordinates)))

    begin, end = -1, -1
    min_distance = -1
    for v in (range(1, len(coordinates))):
        new_distance = euclidean_distance(coordinates[0], coordinates[v], price, money_list[0])
        if new_distance < min_distance or min_distance == -1:
            begin = 0
            end = v
            min_distance = new_distance
    permutation.extend([begin, end])
    not_used.remove(begin)
    not_used.remove(end)

    for i in tqdm(range(len(coordinates) - 2)):
        new_vertex = -1
        min_distance = -1

        for u in not_used:
            vertex_distance = -1
            for v in permutation:
                new_distance = euclidean_distance(coordinates[u], coordinates[v], price, money_list[u])
                if new_distance < vertex_distance or vertex_distance == -1:
                    vertex_distance = new_distance
            if vertex_distance < min_distance or min_distance == -1:
                new_vertex = u
        not_used.remove(new_vertex)

        split_place = -1
        min_distance = -1
        for j in range(i + 2):
            new_distance = replacement_loss(coordinates[new_vertex], coordinates[permutation[j]],
                                            coordinates[permutation[(j + 1) % (i + 2)]], price, money_list[new_vertex])
            if new_distance < min_distance or min_distance == -1:
                split_place = j
                min_distance = new_distance

        permutation = permutation[0:split_place + 1] + \
                      [new_vertex] + permutation[split_place + 1:i + 2]
    return permutation


# k, M - для отсчения, будем исользовать только в первой задаче
n, price, k, M, coordinates, money_list = read_input()
solution = solve_tsp_nearest_insertion(coordinates, price, money_list)

for i in range(len(solution)):
    solution[i] += 1
solution.append(1)
res = ' '.join(list(map(str, solution)))

with open('data/ans.txt', 'w') as file:
    file.write(res)

############ FIRST CAPTAIN MIPT ###############
# window = []
# mo = 0
# res = []
# for i in solution:
#     if len(window) >= k:
#         mo = 0
#         for el in window:
#             mo += money[el-1]
#         print('mo1=', mo)
#         if mo > M:
#             print('win1=', window)
#             del window[len(window)-1]
#         else:
#             res.append(window[0])
#             del window[0]
#     else:
#         mo = 0
#         for el in window:
#             mo += money[el-1]
#         print('mo2=', mo)
#         if mo > M:
#             print('win2=', window)
#             del window[len(window)-1]
#         else:
#             window.append(i)
#             print('win3=', window)
#


# print(len(res))
# print('---------------------------')
# res = ' '.join(list(map(str, res)))
#
# print(res)
