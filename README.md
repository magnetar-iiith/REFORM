# Overview
- In this code we simulate our crowdsourcing model.
- We consider 1000 tasks, 750 available agents in each round
- Tasks have an answer space = {0,1,2}
- Alpha for REFORM and RPTSC is 10
- We assume the available agents constitute 60% TAs, 40% RAs (other distributions can be similarly plugged-in)

# Usage
- Require Python3 environment
- Run Command: python3 simulation.py

## Code Description
- `get_rewards` runs for the simulation for given rounds computing rewards for Trustworthy agent (TA) and Random agent (RA)
- `Report` generates reports according to the agents strategies
- `Prime` computes PRIME scores for all the agents in every round
- `Sample` randomly samples reports from different tasks to compute the rewards
- `RPTSC` computes rewards for agents using RPTSC reward scheme
- `REFORM` computes rewards for agents in REFORM framework using RPTSC reward scheme