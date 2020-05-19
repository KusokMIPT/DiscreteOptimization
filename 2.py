from random import random
from typing import List

import numpy as np
from scipy.optimize import linprog


class MinimumVertexCover:
    def __init__(self, n_columns: int, n_rows: int, rows_list: List[List[int]], weights: List[int]):
        self.n_columns, self.n_rows = n_columns, n_rows

        self.rows_list = rows_list.copy()
        self.weights = weights.copy()

    def solve(self) -> None:
        cond_matrix = np.zeros((self.n_rows, self.n_columns))

        for i, row in enumerate(self.rows_list):
            for current_col in row:
                cond_matrix[i][current_col] = -1

        x_list = linprog(c=self.weights, A_ub=cond_matrix.T,
                         b_ub=-np.ones(self.n_columns), bounds=(0, 1)).x

        covered_col, used_rows = set(), set()

        while len(covered_col) != self.n_columns:
            for i, v in enumerate(x_list):
                if (i + 1 not in used_rows) and (random() <= v):
                    used_rows.add(i + 1)
                    [covered_col.add(el) for el in self.rows_list[i]]
                    # covered_col = covered_col.union(set(self.rows_list[i]))

        return [i + 1 for i, el in enumerate(used_rows) if el]


def reading_input():
    n_columns, n_rows = map(int, input().split())

    graph = list()
    weights = list()

    for i in range(n_rows):
        string = list(map(int, input().split()))
        weights.append(string[0])

        graph.append(string[1:])

    return n_columns, n_rows, graph, weights


minimum_vertex_cover = MinimumVertexCover(*reading_input())
print(" ".join(map(str, minimum_vertex_cover.solve())))

