# PoS - Prospective Reorganization Attack
# three slots per attack
import math

N = 28224
C = 2400
# for attacks without proposer boost.... 
# for p in [0.01, 0.02, 0.03, 0.04, 0.05]:

# for attacks with proposer boost 
for p in [0.0334, 0.0667, 0.1001]:
    p_v = 1 - pow(1-p, N)
    p_p = p * p * (1-p)
    p_one = p_v * p_p 
    p_day = 1 - pow(1-p_one, C)
    print(p, p_day)

