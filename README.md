# Breaking the Privacy Barrier: On the Feasibility of Reorganization Attacks on Ethereum Private Transactions


### Abstract

In Ethereum, private transactions are typically more profitable but
can sometimes be leaked into the public network before on-chain
posting. Motivated by the huge profits of these private transactions,
we propose reorganization attacks, enabling malicious validators to
actively leak private transactions for profits. While prior research
on reorganization attacks has focused on consensus security, our
work is the first study shedding light on the economic implications
of exploiting private transactions. Through theoretical analysis and
extensive simulations, we confirm the effectiveness of our attacks.
Additionally, we comprehensively measure real-world datasets
spanning two years from 2022 to 2023 consisting of 36,777,863
private transactions for profit analysis, uncovering that the most
lucrative private transactions are often tied to Maximum Extractable
Value (MEV) and Decentralized Finance (DeFi) incidents. We further
verify the practicability and feasibility of our attacks by evaluating
real-world cases that align with attack patterns. We also compare
our attacks in both Proof-of-Work (PoW) and Proof-of-Stake (PoS)
Ethereum, revealing that the latter are virtually risk-free due to
predictable validators’ duties. Our findings offer valuable insights
into the economics of exploiting private transactions, potential
vulnerabilities, and consensus security, laying the groundwork for
future research and risk mitigation

### Private Transactions Data


We got the privatex transactions from [mempool-data-program](https://docs.blocknative.com/mempool-data-program) of blocknative.Thanks to them for providing the data to the public!
This collection contains over 8TB of archive data representing more than 16 billion transaction detection events since November 1st, 2019. 
This dataset covers major scenarios the network has encountered over the years, including massive surges in traffic, huge gas spikes, bidding wars, the launch of MEV-boost, the price of ETH collapsing, EIP-1559, Black Thursday, and major hacks.


### MEV Data
We obtain the MEV dataset from the [ZeroMEV API](https://data.zeromev.org/docs/).The MEV  types are as follows:

-> arb: An arbitrage transaction allowing the extractor to profit from price discrepancies between exchanges.
-> frontrun: The frontrun transaction in a sandwich. This initiates the attack and moves the price against the victim.
-> sandwich: A victim transaction in a sandwich. There can be one or more of these per attack.
-> backrun: The backrun in a sandwich, allowing the attacker to close their position and extract a profit.
-> liquid: Refers to a liquidation event in a DeFi lending protocol.
-> swap: Swaps are included to provide volume data for non-MEV transactions.


### Block/Slot Data
We acquire fork blocks, including votes, block hashes, proposer,etc., from the [Beacon Chain API](https://beaconcha.in/) & [Quicknode API](https://www.quicknode.com/docs/ethereum).We all got authorized to use these API.
