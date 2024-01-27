# PoS - Prospective Reorganization Attack
# three slots per attack
from __future__ import annotations
from dataclasses import dataclass, field
import random
import os
import sys

# # , "celsius": 0.0075, "whale-0xeab8": 0.0059
# # from https://beaconcha.in/pools - July 14, 2023
# top_10 = {"lido": 0.1919, "coinbase": 0.0609, "rocketpool": 0.031, "binance": 0.031, "kraken": 0.0242, "staked.us": 0.0181,
#           "whale-0x5d7": 0.0159, "bitcoin": 0.0135, "stakefish": 0.0112, "figment": 0.0079}
# need to update the data on 2024

@dataclass
class Validator(object):
    ID: int
    IsAttack: bool


@dataclass
class Epoch(object):
    N: int
    S: int
    T: int
    A: int # attacker controlled validator number
    Validators: list
    Committees: list # 32 slots with committees in each slot
    Proposers: list

    def init(self, n, attack_percentage):
        self.N = n
        self.S = 32
        self.T = self.N * self.S
        self.A = int(self.T * attack_percentage)

    def prepare_validators(self):
        for i in range(self.T):
            if i < self.A:
                self.Validators.append(Validator(i, True))
            else:
                self.Validators.append(Validator(i, False))

    def assign_commmitees_per_epoch(self):
        random.shuffle(self.Validators)
        for i in range(self.S):
            start_index = i*self.N
            end_index = (i+1)*self.N
            self.Committees.append(self.Validators[start_index:end_index])

    # proposer is the first committee member in default
    def proposers_per_epoch(self):
        for i in range(self.S):
            proposer = self.Committees[i][0]
            self.Proposers.append(proposer)

def get_one_epoch(committee_size, attacker_per):
    # deal with one epoch
    epoch = Epoch(0, 0, 0, 0, [], [], [])
    epoch.init(committee_size, attacker_per) # epoch.init(10, 0.1)
    epoch.prepare_validators()
    epoch.assign_commmitees_per_epoch()
    epoch.proposers_per_epoch()
    return epoch


def has_attack_per_day():
    for i in range(225):
        epoch = get_one_epoch(global_N, global_ap)
        for j in range(32):
            # 2.1: slot j proposer is attacker
            if epoch.Proposers[j].IsAttack:
                if j <= 29:
                    # 2.2: slot j+2 proposer is attacker and slot j+1 proposer is not attacker
                    if epoch.Proposers[j+2].IsAttack and not epoch.Proposers[j+1].IsAttack:
                        # 2.3: there is at least one validator in slot in the committee belonging to
                        has_attacker = False
                        this_committee = epoch.Committees[j]
                        for com in this_committee:
                            if com.IsAttack:
                                has_attacker = True 
                                break 
                        if has_attacker:
                            return True
    return False

global_N = int(sys.argv[1])
global_ap = float(sys.argv[2])
rounds = int(sys.argv[3])
os.system("rm " + "pos_pro_sim_" + str(global_N) + "_" + str(global_ap) + ".txt")
gobalf = open("pos_pro_sim_" + str(global_N) + "_" + str(global_ap) + ".txt", "a")
attack2_p_one_day = 0.0
for round_index in range(rounds):
    if has_attack_per_day():
        attack2_p_one_day += 1 
    if round_index % 100 == 0:
        print("done ->:", global_ap, "round_index:", round_index, "attack2_p_one_day:", attack2_p_one_day)
        gobalf.write("round:" + str(round_index) + " attack2_p_one_day:" + str(attack2_p_one_day) + "\n")        

gobalf.write("final pos_pro_one_day:" + str(attack2_p_one_day/rounds))
gobalf.close()