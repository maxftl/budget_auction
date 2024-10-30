import scipy
from collections import deque
from itertools import combinations
import networkx

DUMMY_ITEM = -1

def getRestrictedDemandSet(valuation, price, budget, permited):
    utilities = [v-p if p <= budget and i in permited else -1 for i,(v,p) in enumerate(zip(valuation,price))]
    max_utility = max(utilities) if len(utilities) > 0 else 0
    if max_utility < 0:
        return set([DUMMY_ITEM])
    demand_set = {i for i, u in enumerate(utilities) if u == max_utility}
    if max_utility == 0:
        demand_set.add(DUMMY_ITEM)
    return demand_set

def isOverdemanded(demandSets, setOfGoods):
    i = 0
    for demandSet in demandSets:
        if demandSet.issubset(setOfGoods):
            i += 1
    return i > len(setOfGoods)

def getMinimallyOverdemandedSet(demandSets, goods):
    for card in range(1,len(demandSets) + 1):
        for subset in combinations(goods, card):
            subset = set(subset)
            if isOverdemanded(demandSets, subset):
                return subset
    return None

def findBidderWithDemandJump(oldDemands, newDemands):
    for i,(old, new) in enumerate(zip(oldDemands, newDemands)):
        if not old.issubset(new):
            return (i,old.difference(new))
    return (-1,None)

def auctionStep(valuations, prices, budgets, permited_items, goods):
    demandSets = [getRestrictedDemandSet(valuation, prices, budget, permited)
                  for valuation, budget, permited in zip(valuations,budgets,permited_items)]
    minimallyOverdemanded = getMinimallyOverdemandedSet(demandSets, goods)
    if minimallyOverdemanded is None:
        return (prices, permited_items, True)
    newPrices = prices.copy()
    for j in minimallyOverdemanded:
        newPrices[j] += 1
    newDemandSets = [getRestrictedDemandSet(valuation, newPrices, budget, permited)
                  for valuation, budget, permited in zip(valuations,budgets,permited_items)]
    (bidderAtLimit, excludedGoods) = findBidderWithDemandJump(demandSets, newDemandSets)
    if bidderAtLimit == -1:
        return (newPrices, permited_items, False)
    else:
        permited_items[bidderAtLimit] = permited_items[bidderAtLimit].difference(excludedGoods)
        return (prices, permited_items, False)
    
def getAllocation(demandSets, prices, bidders, goods):
    graph = networkx.DiGraph()
    source = (-1,-1)
    sink = (2,2)
    for bidder, demand in enumerate(demandSets):
        for good in demand:
            weight = 1
            if good >= 0 and prices[good] > 0:
                weight = 0
            graph.add_edge((0,bidder),(1,good),capacity=1,weight=weight)
            graph.add_edge(source, (0,bidder), capacity=1, weight=0)
    for good in goods:
        graph.add_edge((1,good),sink,capacity=1,weight=0)
    graph.add_edge((1,DUMMY_ITEM),sink, capacity = 10000, weight = 0)
    max_flow_min_cost = networkx.max_flow_min_cost(graph, source, sink)
    result = {}
    for b in bidders:
        for g in demandSets[b]:
            if max_flow_min_cost[(0,b)][(1,g)] > 0:
                result[b] = g
    return result


def runAuction(valuations, budgets):
    num_bidders = len(valuations)
    num_goods = len(valuations[0])

    bidders = list(range(num_bidders))
    goods = list(range(num_goods))
    permited_items = [
        set(goods) for _ in range(num_bidders)
    ]
    prices = [0] * num_goods
    while True:
        (prices, permited_items, done) = auctionStep(valuations, prices, budgets, permited_items, goods)
        if done:
            break
    demandSets = [getRestrictedDemandSet(valuation, prices, budget, permited)
                  for valuation, budget, permited in zip(valuations,budgets,permited_items)]
    allocation = getAllocation(demandSets, prices, bidders, goods)
    return {
        'prices': prices,
        'allocation': allocation
    }

if __name__ == '__main__':
    print(runAuction([[13]],[4]))