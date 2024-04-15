#! /bin/bash

# for attacks without proposer boost.
# for ap in 0.01 0.02 0.03 0.04 0.05

# for attacks with proposer boost 
for ap in 0.0334 0.0667 0.1001
do
    python3 pos-pro-sim.py 28224 $ap 10000 &
done
