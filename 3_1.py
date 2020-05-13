from typing import List
from typing import Dict

import numpy as np
import sys

from scipy.optimize import linprog

class Knapsack_solution(object):
    def __init__(self, knapsack_volume, items_num, volume_list, value_list):
        self.knapsack_volume = knapsack_volume
        self.items_num = items_num
        self.volume_list = volume_list
        self.value_list = value_list

    def _sort_by_cost_per_volume(self):
        item_sorted_list = sorted([(self.value_list[i], self.volume_list[i]) for i in range(self.items_num)],
                                  reverse=True,
                                  key=lambda x: x[0] / x[1])
        self.value_list = np.array([item_sorted_list[i][0] for i in range(self.items_num)])
        self.volume_list = np.array([item_sorted_list[i][1] for i in range(self.items_num)])

    def _greedy_solution(self) -> int:
        current_volume_1 = self.knapsack_volume
        current_volume_2 = self.knapsack_volume

        sorted_things_1 = sorted([(self.value_list[i], self.volume_list[i]) for i in range(self.items_num)],
                                 reverse=True,
                                 key=lambda x: x[0] / x[1])
        sorted_things_2 = sorted([(self.value_list[i], self.volume_list[i]) for i in range(self.items_num)],
                                 reverse=True)

        ans_1 = 0
        ans_2 = 0

        def f(diff1, diff2):
            # print(diff1, diff2)
            nonlocal current_volume_1, current_volume_2, ans_1, ans_2

            if diff1[1] < current_volume_1:
                current_volume_1 -= diff1[1]
                ans_1 += diff1[0]

            if diff2[1] < current_volume_2:
                current_volume_2 -= diff2[1]
                ans_2 += diff2[0]

        [f(diff1, diff2) for (diff1, diff2) in zip(sorted_things_1, sorted_things_2)]

        return max(ans_1, ans_2)

    def solution(self) -> object:
        self._sort_by_cost_per_volume()

        down = self._greedy_solution()
        # print(down)
        return find_up(self.knapsack_volume, self.items_num, self.volume_list, self.value_list, 0, down)


# перебор с отсечением
def find_up(knapsack_volume: int, items_num: int, volume_list: List[int], value_list: List[int], gained: int,
            best: int):
    def find_best(knapsack_volume, items_num, volume_list, value_list, gained):
        nonlocal best

        opt = 0
        W = knapsack_volume
        for i in range(items_num - 1, -1, -1):
            if W < volume_list[i]:
                opt += value_list[i] * W / volume_list[i]
                break
            else:
                opt += value_list[i]
                W -= volume_list[i]

        opt = int(opt)

        if items_num == 1:
            if volume_list[items_num - 1] <= knapsack_volume:
                gained += value_list[items_num - 1]
            best = max(best, gained)
            return

        if gained + opt < best:
            return

        find_best(knapsack_volume, items_num - 1, volume_list, value_list, gained)

        if volume_list[items_num - 1] <= knapsack_volume:
            find_best(knapsack_volume - volume_list[items_num - 1], items_num - 1, volume_list, value_list,
                      gained + value_list[items_num - 1])

    sys.setrecursionlimit(2 * items_num + 1)

    find_best(knapsack_volume, items_num, volume_list[::-1], value_list[::-1], gained)
    return best


def reading_input():
    knapsack_volume = int(input())
    items_num = int(input())

    volume_list = []
    value_list = []
    for i in range(items_num):
        x, y = map(int, input().split())
        volume_list.append(x)
        value_list.append(y)

    return knapsack_volume, items_num, volume_list, value_list


s = Knapsack_solution(*reading_input())

print(s.solution())
