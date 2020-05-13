from collections import OrderedDict
from typing import List

# Leave the whole “solve_bp_decision” function intact
def solve_bp_decision(items: List[float], n_bins: int) -> bool:
    def able_to_pack(items: List[float], bin_capacities: List[float]) -> bool:
        return items == [] or any(
            able_to_pack(
                items[:-1],
                bin_capacities[:i] + [capacity - items[-1]] + bin_capacities[(i + 1):]
            )
            for i, capacity in enumerate(bin_capacities) if capacity >= items[-1]
        )

    return able_to_pack( sorted(items), [1.0] * n_bins )


def solve_bp_evaluation(items: List[float]) -> int:
    test_amount = len(items)
    while solve_bp_decision(items, test_amount):
        test_amount -= 1
    return test_amount + 1


def solve_bp_search(items: List[float]) -> List[int]:
    """
    :param items: лист с весами предметов
    :return: лист с номером пакета для каждого предмета
    """

    ans = OrderedDict({i: -1 for i in range(len(items))})  # dict like {вещь : пакет}
    current_bin = 1  # номер пакета
    optimal_number = solve_bp_evaluation(items)  # оптимальное число пакетов

    for i in range(len(items)):
        if ans[i] == -1:
            ans[i] = current_bin

            for j in range(len(items)):
                if ans[j] != -1:
                    continue
                upd = items[j]
                items[i] += upd
                items[j] = 0
                if solve_bp_evaluation(items) != optimal_number:
                    items[j] = upd
                    items[i] -= upd
                else:
                    ans[j] = current_bin
            current_bin += 1

    return list(ans.values())

