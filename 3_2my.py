def greed(total_1, number_1):  # return lower bound
    if number_1 == number:
        return 0
    vol = 0
    for i in range(number_1, number):
        vol += Bin[i]
        if vol > total_1:
            vol -= Bin[i]
    return float(vol)


def FakeLp(total_3, number_3):
    if number_3 == number:
        return 0
    vol = 0
    price = 0
    for i in range(number_3, number):
        vol += Bin[i]
        if vol <= total_3:
            price += Bin[i]
        else:
            vol -= Bin[i]
            price += total_3 - vol
            break
    return float(price)


def attempt(total_c, number_c, cost):
    r = [0 for i in range(number - number_c)]
    numc = number_c
    global Min
    ch = 1
    var_xi = 0
    while ch == 1:
        while number_c != number and Bin[number_c] > total_c:
            number_c += 1
        if number_c == number:
            return cost, r
        lp = FakeLp(total_c, number_c + 1)
        if Min > cost + lp:
            total_c -= Bin[number_c]
            cost = total - total_c
            r[number_c - numc] = 1
            number_c += 1
            continue
        gr = greed(total_c, number_c)
        if Min <= gr + cost:
            Min = gr + cost
        ch = 1 if gr + cost >= lp else 0
        if ch:
            total_c -= Bin[number_c]
            cost = total - total_c
            r[number_c - numc] = 1
            number_c += 1
        else:
            var_xi, r_c = attempt(total_c - Bin[number_c], number_c + 1, cost + Bin[number_c])
            if var_xi > Min:
                Min = var_xi
            if float(var_xi) >= cost + lp:
                r[number_c - numc] = 1
                for i in range(len(r_c)):
                    r[len(r) - len(r_c) + i] = r_c[i]
                return var_xi, r
            else:
                gr = greed(total_c, number_c + 1)
                if Min < gr + cost:
                    Min = gr + cost
                    number_c += 1
                    ch = 1
    if number_c == number:
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


# INPUT
number = int(input())  # number_of_items
total = float(input())  # total_knapsack_volume
import numpy as np

Bin = [float(i) for i in input().split()]


def sort_key(i):  # sort Bin in volume = price order
    return -i


Bin_stability = []  # чтобы сохранить устойчивость перебора, тк Bin сортируется и attempt выдает ответ для Bin
for i in range(number):
    Bin_stability.append(Bin[i])
Bin.sort(key=sort_key)
Bin_copy = []
for i in range(number):
    Bin_copy.append(Bin[i])
Bin = np.asarray(Bin)
ri = [0 for i in range(0, number)]
ri_sability = [0 for i in range(number)]
num = 0  # number of bin
while (number != 0):
    Min = greed(total, 0)
    Bin_at = []
    var, r_at = attempt(total, 0, 0)
    count_0 = 0
    j = 0
    ii = 0
    for i in range(number):
        if r_at[i] != 0:
            while j != count_0:
                if ri[ii] == 0:
                    j += 1
                ii += 1
            while ri[ii] != 0:
                ii += 1
            ri[ii] = 1 + num
        else:
            count_0 += 1
            Bin_at.append(Bin[i])
    num += 1
    Bin = Bin_at
    number = len(Bin)
for i in range(len(ri)):
    ri_sability[Bin_stability.index(Bin_copy[i])] = ri[i]
    Bin_stability[Bin_stability.index(Bin_copy[i])] = 0
for i in range(len(ri_sability)):
    print(ri_sability[i], end=" ")
