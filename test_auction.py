from auction import runAuction

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