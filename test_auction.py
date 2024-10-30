from auction import *

def test_demand_set_restriction():
    valuation = [6,2]
    price = [3,0]
    budget = 0
    permited = {0,1}
    demand_set = getRestrictedDemandSet(valuation, price, budget, permited)
    assert(demand_set == {1})


def test_one_bidder_one_item():
    valuations = [[5]]
    budgets  = [3]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [0])
    assert(outcome['allocation'][0] == 0)

def test_two_bidders_one_item():
    valuations = [
        [5],
        [3]
    ]
    budgets = [10,10]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [3])
    assert(outcome['allocation'][0] == 0)
    assert(outcome['allocation'][1] == -1)

def test_two_bidders_tight_budget():
    valuations = [
        [1000],
        [2]
    ]
    budgets = [1,1000]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [1])
    assert(outcome['allocation'][0] == -1)
    assert(outcome['allocation'][1] == 0)

def test_two_bidders_two_goods():
    valuations = [
        [10,7],
        [6,2]
    ]
    budgets = [100,100]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [3,0])
    assert(outcome['allocation'][0] == 1)
    assert(outcome['allocation'][1] == 0)

def test_two_bidders_two_goods_budget():
    valuations = [
        [10,7],
        [6,2]
    ]
    budgets = [100, 0]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [0,0])
    assert(outcome['allocation'][0] == 0)
    assert(outcome['allocation'][1] == 1) 

def test_example_5_from_paper():
    valuations = [
        [100,0],
        [100,100],
        [0,100]
    ]
    budgets = [100,50,1]
    outcome = runAuction(valuations, budgets)
    assert(outcome['prices'] == [1,1])
    assert(outcome['allocation'][0] == 0)
    assert(outcome['allocation'][1] == 1)
    assert(outcome['allocation'][2] == DUMMY_ITEM)
