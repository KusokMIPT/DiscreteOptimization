import itertools
import datetime
import math
from collections import OrderedDict


def read_input():
    number_of_items = int(input())
    max_bin_volume = int(input())
    items = []
    for i in range(number_of_items):
        items.append(int(input()))

    return max_bin_volume, items


class Bin:
    max_volume = -1

    def __init__(self):
        self.max_volume = Bin.max_volume
        self.list = []
        self.total_volume = 0

    def add_item(self, item):
        self.list.append(item)
        self.total_volume += item

    def check(self, item):
        return self.total_volume + item < self.max_volume

    def out(self):
        return self.list

    def pop(self):
        self.total_volume -= self.list[-1]
        del (self.list[-1])

    def __str__(self):
        return str(self.list)


def ans_getting(list_items, list_bins):
    pre_ans = {}
    for num_, bin in enumerate(list_bins):
        for things in bin.out():
            pre_ans[things] = num_

    ans = []
    for things in list_items:
        ans.append(pre_ans[things] + 1)

    return ans


class BinPackingSolver():
    def __init__(self, max_bin_volume, items):
        self.n = len(items)
        self.items = items
        Bin.max_volume = max_bin_volume

        self.bins = [Bin()]

    def solve(self):
        ' рекурсия по эелментам (k_element - индекс элемента, curBin - количество бина) '

        ans = []
        min_n_bins = math.ceil(sum(self.items) / Bin.max_volume)
        cur_min_n_bins = self.n

        def full_search(k_element: int):
            nonlocal ans, cur_min_n_bins

            if len(self.bins) > min_n_bins:
                return

            if cur_min_n_bins > min_n_bins:
                return

            if k_element == self.n - 1:
                ind_for_put_k_element = -1

                for i in range(len(self.bins)):
                    if self.bins[i].check(self.items[k_element]):
                        ind_for_put_k_element = i

                if ind_for_put_k_element > 0:
                    self.bins[ind_for_put_k_element].add_item(self.items[k_element])

                    if len(self.bins) < cur_min_n_bins:
                        ans = ans_getting(self.items, self.bins)
                        cur_min_n_bins = len(self.bins)

                    self.bins[ind_for_put_k_element].pop()
                else:
                    self.bins.append(Bin())
                    self.bins[-1].add_item(self.items[k_element])

                    if len(self.bins) < cur_min_n_bins:
                        ans = ans_getting(self.items, self.bins)
                        cur_min_n_bins = len(self.bins)

                    del (self.bins[-1])
                return

            for cur_bin in self.bins:
                if cur_bin.check(self.items[k_element]):
                    cur_bin.add_item(self.items[k_element])
                    full_search(k_element + 1)
                    cur_bin.pop()

            self.bins.append(Bin())
            self.bins[-1].add_item(self.items[k_element])
            full_search(k_element + 1)
            self.bins[-1].pop()
            del self.bins[-1]

            return

        full_search(0)

        return ans


solver = BinPackingSolver(*read_input())
ans = solver.solve()
for i in ans:
    print(i, end=" ")
