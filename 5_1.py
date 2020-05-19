import sys
from typing import List, Tuple, Set

import numpy as np

INF = sys.maxsize


def read_input():
    line = input()
    graph = [[]]
    terminal_cnt, node_cnt = -1, -1
    terminal_vertex = []

    while True:
        if 'Nodes ' in line:
            trash, node_cnt = line.split()
            node_cnt = int(node_cnt)
            line = input()
            trash, edge_cnt = line.split()
            edge_cnt = int(edge_cnt)

            graph = [[] for i in range(node_cnt)]

            for i in range(edge_cnt):
                line = input().split()
                graph[int(line[1]) - 1].append((int(line[2]) - 1, int(line[3])))
                graph[int(line[2]) - 1].append((int(line[1]) - 1, int(line[3])))

        if 'Terminals ' in line:
            trash, terminal_cnt = line.split()
            terminal_cnt = int(terminal_cnt)

            for i in range(terminal_cnt):
                line = input().split()
                terminal_vertex.append(int(line[1]) - 1)
            break

        line = input()

    return graph, terminal_vertex, edge_cnt


def read_input2(read_from_file=True):
    graph_matrix = [[(40, 5)], [(7, 8), (20, 7), (31, 2), (18, 5), (35, 8)], [(10, 7)], [(4, 8), (35, 6)],
                    [(3, 8), (27, 8), (29, 4)], [(16, 7), (41, 9)], [(28, 7), (19, 3)], [(1, 8)], [(28, 5)],
                    [(21, 6)],
                    [(2, 7), (35, 9)], [(20, 7)], [(49, 1)], [(30, 9), (19, 7)], [(29, 1), (39, 10)],
                    [(19, 8), (29, 2)], [(5, 7), (41, 6), (20, 5)], [(18, 2), (27, 1), (42, 1), (20, 10)],
                    [(17, 2), (1, 5)],
                    [(6, 3), (13, 7), (15, 8), (26, 2), (37, 8), (39, 10), (47, 2), (21, 2), (33, 10)],
                    [(1, 7), (11, 7), (16, 5), (17, 10), (21, 2)],
                    [(9, 6), (19, 2), (20, 2), (39, 8), (42, 7), (40, 8)], [(39, 3)], [(27, 5), (43, 8)],
                    [(33, 4), (40, 5)], [(44, 6)], [(19, 2), (33, 4)], [(17, 1), (4, 8), (23, 5), (44, 1)],
                    [(6, 7), (8, 5), (32, 7)], [(4, 4), (14, 1), (15, 2), (33, 2)], [(13, 9)], [(1, 2)],
                    [(28, 7), (34, 3)], [(24, 4), (26, 4), (19, 10), (29, 2)], [(32, 3)],
                    [(1, 8), (3, 6), (10, 9), (38, 7), (48, 9), (49, 10), (40, 2)], [(46, 3)], [(19, 8)],
                    [(35, 7), (43, 3)], [(19, 10), (21, 8), (14, 10), (22, 3)],
                    [(0, 5), (21, 8), (24, 5), (35, 2), (43, 7), (46, 7)], [(16, 6), (5, 9), (45, 10)],
                    [(17, 1), (21, 7)], [(40, 7), (23, 8), (38, 3)], [(25, 6), (27, 1), (46, 10)], [(41, 10)],
                    [(40, 7), (36, 3), (44, 10)], [(19, 2)], [(35, 9)], [(35, 10), (12, 1)]]

    terminals = [47, 48, 21, 34, 26, 11, 36, 33, 23]
    vertex_number = 50

    return graph_matrix, terminals, vertex_number


def dijkstra(graph_edges: List[List[Tuple[int, int]]],
             start_vertex: int,
             vertex_number: int):
    """ обычный дейкстра для графа в виде таблица смежности"""
    dist = [INF] * vertex_number
    pred = [0] * vertex_number

    def relaxation():
        nonlocal graph_edges, dist, pred, curv
        for j in range(len(graph_edges[curv])):
            way = graph_edges[curv][j]

            if dist[curv] + way[1] < dist[way[0]]:
                dist[way[0]] = dist[curv] + way[1]
                pred[way[0]] = curv


    dist[start_vertex] = 0

    used = [False] * vertex_number

    for i in range(vertex_number):
        curv = -1
        for vertex in range(vertex_number):
            if not used[vertex] and (curv == -1 or dist[vertex] < dist[curv]):
                curv = vertex

        if dist[curv] == INF:
            break
        used[curv] = True

        # релаксация
        relaxation()

    return dist, pred


def metric_closure(graph_edges: List[List[Tuple[int, int]]], terms: List[int], n: int) -> \
        List[List[int]]:
    closure = np.zeros((len(terms), len(terms)))

    for i in range(len(terms)):
        distance_to_all = dijkstra(graph_edges, terms[i], n)[0]

        for j in range(n):
            if j in terms:
                closure[i][terms.index(j)] = distance_to_all[j]
    return closure


def find_suitable_vertex(incident_vertexes: List[int],
                         used: Set[int],
                         terms: List[int]) -> Tuple[int, int]:
    """find vertex with minimum weight"""

    weight, vertex = INF, INF

    for i in range(len(incident_vertexes)):

        if incident_vertexes[i] < weight and terms[i] not in used:
            weight = incident_vertexes[i]
            vertex = terms[i]
    return weight, vertex  # вес ребра, номер последний вершины - конец ребра


def path_recovery(mst_tree: List[int]):
    '''по вершинам из полученного mst восстанавлием путь с помощью той же дейкстры'''
    path_way = set([])

    for edge in mst_tree:
        distance_to_all, pred_arr = dijkstra(graph_matrix, edge[0], vertices_number)

        path = []
        cur_v = edge[1]

        path.append(cur_v)
        while cur_v != edge[0]:
            cur_v = pred_arr[cur_v]
            path.append(cur_v)
        path.reverse()

        for i in range(len(path) - 1):
            path_way.add((path[i], path[i + 1]))

    return path_way


class Edge:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight

    def __str__(self):
        return str((self.x, self.y, self.weight))


class DSU:
    def __init__(self, vertex_count):
        self.pr = [i for i in range(vertex_count)]
        self.size = [1] * vertex_count

    def unite(self, u, v):
        u = self.get_root(u)
        v = self.get_root(v)
        if u == v:
            return False
        if self.size[u] > self.size[v]:
            u, v = v, u
        self.pr[u] = v
        self.size[v] += self.size[u]
        return True

    def get_root(self, vertex):
        if self.pr[vertex] == vertex:
            return vertex
        self.pr[vertex] = self.get_root(self.pr[vertex])
        return self.pr[vertex]


def mst_closure(graph_matrix: List[List[int]], terms: List[int]) -> List[int]:
    tree = list()
    considered_vertices = set()
    considered_vertices.add(terms[0])

    cur_tree = terms[1:].copy()
    while cur_tree:
        min_weight = INF

        for vertex in considered_vertices:
            possible_min_weight, possible_end = find_suitable_vertex(
                graph_matrix[terms.index(vertex)],
                considered_vertices,
                terms)

            if possible_min_weight < min_weight:
                del_vertex = vertex
                edge_end = possible_end
                min_weight = possible_min_weight

        considered_vertices.add(edge_end)
        cur_tree.remove(edge_end)
        tree.append((del_vertex, edge_end))

    return tree


class SteinerTree():
    def __init__(self, graph_matrix, terminals, n_vertex):
        self.graph = graph_matrix
        self.terminals = terminals
        self.vertices_number = n_vertex

    def solve(self):
        mcl = metric_closure(self.graph, self.terminals, self.vertices_number)
        mst_tree = mst_closure(mcl, self.terminals)

        return set(list((a, b) if a <= b else (b, a) for a, b in path_recovery(mst_tree)))


graph_matrix, terminals, vertices_number = read_input()
steinertree = SteinerTree(graph_matrix, terminals, vertices_number)
ans = steinertree.solve()

# with open('data/ans5_1.txt', 'w') as file:
#     for el in ans:
#         file.write('{} {}\n'.format(el[0] + 1, el[1] + 1))

for vertx in ans:
    print('{} {}'.format(vertx[0] + 1, vertx[1] + 1))
