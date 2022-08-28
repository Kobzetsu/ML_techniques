
import math
from sklearn import tree
import pandas as pd
import numpy as np



def WOE(gap_bads, bads, gap_goods, goods):
    bads_share = (len(gap_bads) + 0.5) / (len(bads) + 0.5) * 1.0
    goods_share = (len(gap_goods) + 0.5) / (len(goods) + 0.5) * 1.0
    val = (goods_share / bads_share)
    return math.log(val), goods_share, bads_share


def binning(x, y, power_depth=20, leaf=2000):
    best_iv = 0

    alldf = pd.concat([x, y], axis=1)

    data_goods = alldf[y == 1]
    data_bads = alldf[y == 0]

    for depth in range(1, power_depth + 1):

        dt = tree.DecisionTreeClassifier(criterion="entropy",
                                         splitter="best", max_depth=depth,
                                         min_samples_leaf=leaf)

        dt.fit(x[:, None], y)

        limit = 10000000
        #  threshold values at nodes without double and leaf value -2
        threshold = list(np.unique([x for x in dt.tree_.threshold if x != -2]))

        # Adding an upper and lower limit
        threshold.append(limit)
        threshold.append(limit * -1)
        # sort
        threshold.sort()
        # prepare gaps with limits
        gaps = []
        for i in range(len(threshold) - 1):
            gaps.append([threshold[i], threshold[i + 1]])

        # calculate WOE for gaps
        woe = 0
        gaps_shares = []
        gaps_woe = []

        data_good = alldf[alldf['y'] == 1]
        data_bad = alldf[alldf['y'] == 0]

        # for each gap
        for gap in gaps:
            # upper and lower limit
            limlow = gap[0]
            limhigh = gap[1]
            # наблюдения в сегменте
            gap_data = alldf[(alldf['x'] >= limlow) & (alldf['x'] <= limhigh)]
            # Goods
            gap_goods = gap_data[gap_data['y'] == 1]
            # Bads
            gap_bads = gap_data[gap_data['y'] == 0]

            # woe for gap
            woe, gap_goods_share, gap_bads_share = WOE(gap_goods, data_good, gap_bads, data_bad)
            # woe for bin
            gaps_shares.append([gap_goods_share, gap_bads_share])
            gaps_woe.append(woe)

        # iv for var bin
        ivs = [(gs[0] - gs[1]) * gw for gs, gw in zip(gaps_shares, gaps_woe)]
        iv = np.sum(ivs)

        # save best bin
        if iv > best_iv:
            best_gaps = gaps
            best_gaps_shares = gaps_shares
            best_gaps_woe = gaps_woe
            best_iv = iv

    return best_iv