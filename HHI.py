import numpy as np

# Херфиндаля-Хиршмена индекс
def HHI(gaps_counts):
    total = 0
    hh_shares = []
    for counts in gaps_counts:
        total += counts[0] + counts[1]
    for counts in gaps_counts:
        hh_shares.append((counts[0] + counts[1]) / total)
    hhi = np.sum([hh ** 2 for hh in hh_shares])
    return hhi