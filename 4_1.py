import random
from math import sqrt


############# not working #############

def reading():
    N = int(input())

    coordinates = [(0, 0)] * N
    for i in range(N):
        # b =  input.split()
        # a = tuple(map(float, input.split()[1:]))
        coordinates[i] = tuple(map(float, input().split()[1:]))
    return coordinates


def euclidean_distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_tour_length(instance, permutation):
    n = len(permutation)
    return sum(euclidean_distance(instance[permutation[i]], instance[permutation[(i + 1) % n]]) for i in
               range(len(permutation)))


def solve_tsp_nearest_neighbour(instance):
    permutation = []
    not_used = set(range(len(instance)))

    new_vertex = random.choice(tuple(not_used))
    permutation.append(new_vertex)
    not_used.remove(new_vertex)

    for i in range(len(instance) - 1):
        new_vertex = -1
        min_distance = -1
        for v in not_used:
            new_distance = euclidean_distance(instance[permutation[i]],
                                              instance[v])
            if new_distance < min_distance or min_distance == -1:
                new_vertex = v
                min_distance = new_distance
        permutation.append(new_vertex)
        not_used.remove(new_vertex)

    return permutation + [permutation[0]]  # с 1 нумерация


def replacement_loss(new, u, v):
    return euclidean_distance(u, new) + \
           euclidean_distance(v, new) - \
           euclidean_distance(u, v)


def solve_tsp_nearest_insertion(instance):
    permutation = []
    not_used = set(range(len(instance)))

    begin, end = -1, -1
    min_distance = -1
    for v in range(len(instance)):
        for u in range(v):
            new_distance = euclidean_distance(instance[u],
                                              instance[v])
            if new_distance < min_distance or min_distance == -1:
                begin = u
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
                new_distance = euclidean_distance(instance[u], instance[v])
                if new_distance < vertex_distance or vertex_distance == -1:
                    vertex_distance = new_distance
            if vertex_distance < min_distance or min_distance == -1:
                new_vertex = u
        not_used.remove(new_vertex)

        split_place = -1
        min_distance = -1
        for j in range(i + 2):
            new_distance = replacement_loss(instance[new_vertex], instance[permutation[j]],
                                            instance[permutation[(j + 1) % (i + 2)]])
            if new_distance < min_distance or min_distance == -1:
                split_place = j
                min_distance = new_distance

        permutation = permutation[0:split_place + 1] + \
                      [new_vertex] + permutation[split_place + 1:i + 2]
    return permutation


print(solve_tsp_nearest_insertion(reading()))
