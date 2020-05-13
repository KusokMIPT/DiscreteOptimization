import numpy as np


def greed_solution(total_1, number_1):  # return lower bound
    if number_1 == number_of_items:
        return 0
    vol = 0
    for i in range(number_1, number_of_items):
        vol += items_size[i]
        if vol > total_1:
            vol -= items_size[i]
    return float(vol)


def like_lp_solution(total_3, number_3):
    if number_3 == number_of_items:
        return 0
    vol = 0
    price = 0
    for i in range(number_3, number_of_items):
        vol += items_size[i]
        if vol <= total_3:
            price += items_size[i]
        else:
            vol -= items_size[i]
            price += total_3 - vol
            break
    return float(price)


def attempt(total_c, number_c, cost):
    r = [0 for i in range(number_of_items - number_c)]
    numc = number_c
    global Min
    ch = 1
    var_xi = 0
    while ch == 1:
        while number_c != number_of_items and items_size[number_c] > total_c:
            number_c += 1
        if number_c == number_of_items:
            return cost, r

        lp = like_lp_solution(total_c, number_c + 1)
        if Min > cost + lp:
            total_c -= items_size[number_c]
            cost = max_bin_volume - total_c
            r[number_c - numc] = 1
            number_c += 1
            continue
        greedy_solution = greed_solution(total_c, number_c)

        Min = min(Min, greedy_solution + cost)
        ch = 1 if greedy_solution + cost >= lp else 0
        if ch:
            total_c -= items_size[number_c]
            cost = max_bin_volume - total_c
            r[number_c - numc] = 1
            number_c += 1
        else:
            var_xi, r_c = attempt(total_c - items_size[number_c], number_c + 1, cost + items_size[number_c])
            if var_xi > Min:
                Min = var_xi
            if float(var_xi) >= cost + lp:
                r[number_c - numc] = 1
                for i in range(len(r_c)):
                    r[len(r) - len(r_c) + i] = r_c[i]
                return var_xi, r
            else:
                greedy_solution = greed_solution(total_c, number_c + 1)
                if Min < greedy_solution + cost:
                    Min = greedy_solution + cost
                    number_c += 1
                    ch = 1
    if number_c == number_of_items:
        return cost
    var_not_xi, r_nc = attempt(total_c, number_c + 1, cost)
    if Min < var_not_xi:
        Min = var_not_xi
    if var_not_xi < var_xi:
        r[number_c - numc] = 1
        for i in range(len(r_c)):
            r[len(r) - len(r_c) + i] = r_c[i]
        return var_xi, r
    else:
        for i in range(len(r_nc)):
            r[len(r) - len(r_nc) + i] = r_nc[i]
        return var_not_xi, r


# '''
#       _____ READING FORMAT: _____
#
# In the BPP format:
# Number of items (n)
# Capacity of the bins (c)
# For each item j (j = 1,...,n):
# Weight (wj)
#
# '''


number_of_items = int(input())
max_bin_volume = float(input())

items_size = [float(i) for i in input().split()]

Bin_stability = []  # чтобы сохранить устойчивость перебора, тк Bin сортируется и attempt выдает ответ для Bin
for i in range(number_of_items):
    Bin_stability.append(items_size[i])

items_size.sort(key=lambda x: -x)
items_size_copy = []

for i in range(number_of_items):
    items_size_copy.append(items_size[i])

items_size = np.asarray(items_size)
ri = [0 for i in range(0, number_of_items)]
ri_sability = [0 for i in range(number_of_items)]

bin_number = 0  # number of bin

while number_of_items != 0:
    Bin_at = []
    var, r_at = attempt(max_bin_volume, 0, 0)
    count_0 = 0
    j = 0
    ii = 0
    for i in range(number_of_items):
        if r_at[i] != 0:
            while j != count_0:
                if ri[ii] == 0:
                    j += 1
                ii += 1
            while ri[ii] != 0:
                ii += 1
            ri[ii] = 1 + bin_number
        else:
            count_0 += 1
            Bin_at.append(items_size[i])
    bin_number += 1
    items_size = Bin_at
    number_of_items = len(items_size)
for i in range(len(ri)):
    ri_sability[Bin_stability.index(items_size_copy[i])] = ri[i]
    Bin_stability[Bin_stability.index(items_size_copy[i])] = 0
for i in range(len(ri_sability)):
    print(ri_sability[i], end=" ")
