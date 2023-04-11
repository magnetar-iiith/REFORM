# Overview
- In this code we simulate our crowdsourcing model.
- We consider 1000 tasks, 750 available agents in each round
- Tasks have an answer space = {0,1,2}
- Alpha for REFORM with RPTSC: 11, Alpha for RPTSC: 10
- We assume the available agents constitute 60% TAs, 40% RAs (other distributions can be similarly plugged-in)

# Usage
- Require Python3 environment
- Run Command: python3 simulation.py

# Code Description
# main
- Main is the start function which runs the functions
- (i) get_rewards function to compute rewards in the framework REFORM and RPSTC for each round


## get_rewards
- It runs for all the rounds computing rewards for TAs and RAs
### Report
- function to generate reports according to their strategies
### TERM
- function to compute TERM scores of agents in every round
### flip
- to randomly pick a quality 
### Sample
- randomly samples reports from different tasks
### RPTSC
- Computes RPTSC rewards
### REFORM
- Computes REFORM rewards
### Plot
- To plot the average rewards we got from function get_rewards
