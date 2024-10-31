from auction import runAuction

# One line per bidder
valuations = [
    [100,1,2],
    [3,1,1]
]

budgets = [1,2]



# Run
outcome = runAuction(valuations, budgets)
print(outcome)
