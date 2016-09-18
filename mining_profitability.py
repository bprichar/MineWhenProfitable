#!/usr/bin/python

HASH_RATE = 120.0 # H/s
POWER_CONSUMPTION = 183.0 # W
ELECTRICITY_COST = 0.02 # $/kWh
REWARD = 0.035 # $/kHh/s
COMPUTER_COST = 500.0 # $

reward_rate = REWARD / 3600 # $/kH
cost_rate = ELECTRICITY_COST * (POWER_CONSUMPTION / HASH_RATE) / 3600 # $/kH
profit = reward_rate - cost_rate # $/kH
profit_rate = profit * HASH_RATE / 1000 # $/s
recoup_time = COMPUTER_COST / profit_rate

print "Profit Rate =$", profit_rate, "/s ($", profit_rate * 3600, "/h)"
print "Recoup time =", recoup_time,"s (", recoup_time / (3600*24), "days)"
