import numpy as np
import tqdm
import datetime


class CaptainMiptSolver:

    def __init__(self, constraints, points):
        self.start_time = datetime.datetime.now()

        self.n, self.p, self.k, self.M = constraints
        self.points = points

    def _count_distances(self):
        ''' считает расстояние между всеми точками '''
        self.distances = np.zeros((self.n, self.n))
        for i in range(self.n - 1):
            p1 = np.array(self.points[i][:2])
            for j in range(i + 1, self.n):
                p2 = np.array(self.points[j][:2])
                self.distances[i, j] = np.sqrt(np.sum((p1 - p2) ** 2))
                self.distances[j, i] = self.distances[i, j]

    def _count_values(self):
        '''считает ценность похода в вершину'''
        self._count_distances()
        self.values = np.zeros((self.n, self.n))
        for i in range(self.n - 1):
            value1 = self.points[i][2]
            for j in range(i + 1, self.n):
                value2 = self.points[j][2]
                self.values[i, j] = value2 - self.distances[i, j] * self.p
                self.values[j, i] = value1 - self.distances[j, i] * self.p

    def _values_NN(self):
        self._count_values()
        point = 0
        visited = {0}
        order = [0]
        savings = np.zeros(self.k - 1)
        i = 0
        while len(visited) < self.n:
            for candidate in np.argsort(-self.values[point]):
                if (candidate not in visited) and (sum(savings) + self.points[candidate][2] <= self.M):
                    savings[i % (self.k - 1)] = self.points[candidate][2]
                    i += 1
                    order.append(candidate)
                    visited = visited.union({candidate})
                    point = candidate
                    break
        return [i + 1 for i in order] + [1]

    def solve(self, method):
        res = self._values_NN()
        print('time elapsed: {} \n'.format(datetime.datetime.now() - self.start_time))
        return res


def read_input(file_name):
    with open(file_name, 'r') as src:
        constraints = tuple(map(int, src.readline().split()))
        points = []
        for line in src:
            x, y, value = tuple(map(int, line.split()))
            points.append((x, y, value))

    return constraints, points


print(' '.join(map(str, CaptainMiptSolver(*read_input('data/data1.txt')).solve('greedy-values'))))

# print(' '.join(map(str, CaptainMiptSolver(data_src).solve('greedy-values'))))
