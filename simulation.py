import numpy as np
import matplotlib.pyplot as plt
import random
import math

'''For REFORM with rho, time is neglected'''
'''Tasks are assumed to be non-binary with answerspace = {0,1,2}'''

rounds = 1000  # no.of rounds
tasks = 50  # no.of tasks in each round
agents = 750  # no.of agents in each round
choices = 3  # no.of choices to report
samples_count = tasks - 1

reports = []    # agents' reports in a round
PRIMEscore = []  # agents' PRIME scores in a round


def flip(P):
    ''' Flip randomly assigns 0 or 1 with prob (p) '''
    return 1 if random.random() < P else 0


def Report():
  ''' Collecting reports submitted by trustworthy and random agents '''
  submn = []
  answers = list(range(choices))
  for _ in range(tasks):
    a = random.choices(answers)
    for _ in range(int(0.6*agents/tasks)):
        submn.append(a)
    for _ in range(int(agents/tasks - int(0.6*agents/tasks))):
      r = random.choices(answers, weights=[0.33, 0.33, 0.33])
      submn.append(r[0])
  return submn


def Peer(A):
    ''' Ramdomly picking agent A's peer '''
    g = A % int(agents/tasks)
    range_valid = [*range(g*int(agents/tasks), A), *
                   range(A+1, (g+1)*int(agents/tasks))]
    P = random.choice(range_valid)
    return P


def Sample(A, P):
    ''' Sampled reports for calc agent A's reward with peer P '''
    samples = []
    sampled_agents = []
    g = A % int(agents/tasks)
    for i in range(tasks):
      if i != g:
        range_valid = [*range((i)*int(agents/tasks), (i+1)*int(agents/tasks))]
        sampled_agents.append(random.choice(range_valid))
    for i in sampled_agents:
        samples.append(reports[int(i)])
    return samples


def RPTSC(A, P, sample):
    ''' RPTSC Reward: Returns actual and optimal reward '''
    alpha1 = 10
    if reports[A] == reports[P]:
        flag = 1
    else:
        flag = 0

    p = (sample.count(reports[A])+flag)/(len(sample)+1)

    if p == 0:
        reward = 0, 0
    else:
        reward = alpha1*(flag/p - 1), alpha1*(1/p-1)

    return reward


def PRIME(curr_round, history):
    ''' PRIME scores calc: Returns PRIMEscore list of all the agents in a round '''
    a = 1
    b = -1
    c = -0.5
    r_s = []

    ''' Calc roundscores '''
    for A in range(agents):
        p = Peer(A)
        if reports[A] == reports[p]:
            flag = 1
        else:
            flag = 0

        sample = Sample(A, p)
        f = (sample.count(reports[A])+flag) / \
            (len(sample)+1)  # calc frequency func
        if flag != 0:
            r_s.append(flag/f)  # round score calc
        else:
            r_s.append(0)

    ''' normalised scores '''
    n_s = []
    for A in range(agents):
        if max(r_s) != min(r_s):
            # normalised round score calc
            n_s.append((r_s[A]-min(r_s))/(max(r_s)-min(r_s)))
        else:
            n_s.append(0)

    history.append(n_s)
    rep_scores = []
    for A in range(agents):
        score = 0
        for rho in range(curr_round+1):
          score = score+history[rho][A]
        rep_scores.append(a*math.exp(b*math.exp(c*score)))  # repscores

    return rep_scores


def REFORM(A, P, sample, rho):
    ''' REFORM rewards '''
    alpha2 = 10
    while rho > 0:
        rho = rho-1
        s = flip(0.6)
        if reports[A] == reports[P]:
            flag = 1
        else:
            flag = 0

        p = (sample.count(reports[A])+flag)/(len(sample)+1)
        if flag == 1:
            return alpha2*(flag/p - 1), alpha2*(1/p-1)
        else:
            if PRIMEscore[A] < PRIMEscore[P] or rho == 0 or (A == agents-1 and s == 1):
                if p == 0:
                    return 0, 0
                else:
                    return -alpha2, alpha2*(1/p-1)
        P = Peer(A)


def get_rewards(rho):
    ''' Calc REFORM and RPTSC rewards for TA and RA '''
    ''' Returns: List of Optimal rewards, REFORM rewards for TA, '''
    ''' RPTSC rewards for TA, REFORM rewards for RA, RPTSC rewards for RA '''
    TA_REFORM = 0
    RA_REFORM = 0
    TA_RPTSC = 0
    RA_RPTSC = 0
    Reform_TA_rewards = []
    Reform_RA_rewards = []
    RPSTC_TA_rewards = []
    RPSTC_RA_rewards = []
    Optimal = 0
    Optimal_list = []
    Opt = 0
    Opt_list = []

    history = []    # 2D list for maintaining agents' history of scores

    for i in range(rounds):
        print("1.Calculating rewards in round ", i, "for rho = ", rho)
        global reports
        reports = Report()
        global PRIMEscore
        PRIMEscore = PRIME(i, history)

        ''' reward for TA '''
        TA = 0
        TA_Peer = Peer(TA)
        TA_sample = Sample(TA, TA_Peer)
        a2, b2 = RPTSC(TA, TA_Peer, TA_sample)
        TA_RPTSC += a2
        Optimal += b2
        Optimal_list.append(Optimal/(i+1))
        RPSTC_TA_rewards.append(TA_RPTSC/(i+1))
        a1, b1 = REFORM(TA, TA_Peer, TA_sample, rho)
        TA_REFORM += a1
        Opt += b1
        Opt_list.append(Opt/(i+1))
        Reform_TA_rewards.append(TA_REFORM/(i+1))

        ''' reward for RA '''
        RA = agents-1
        RA_Peer = Peer(RA)
        RA_sample = Sample(RA, RA_Peer)
        a3, b3 = RPTSC(RA, RA_Peer, RA_sample)
        RA_RPTSC += a3
        RPSTC_RA_rewards.append(RA_RPTSC/(i+1))
        a, b = REFORM(RA, RA_Peer, RA_sample, rho)
        RA_REFORM += a
        Reform_RA_rewards.append(RA_REFORM / (i + 1))
    return np.array(Optimal_list), np.array(Reform_TA_rewards), np.array(RPSTC_TA_rewards), np.array(Reform_RA_rewards), np.array(RPSTC_RA_rewards), np.array(Opt_list)


def plots(opt2, RT2, PT2, RR2, PR2, opt4, RT4, PT4, RR4, PR4, opt8, RT8, PT8, RR8, PR8, O1, O2, O3):
    ''' Plotting the avg rewards of REFORM and RPTSC for different rho's '''
    print("plotting rewards for different rhos")

    R = np.array(list(range(rounds)))
    size = 20
    fig, ((ax3, ax5, ax7), (ax4, ax6, ax8)) = plt.subplots(
        2, 3, sharex=True, sharey=False)
    plt.rcParams["font.weight"] = "bold"

    ax3.set_title("Trustworthy (rho=2)", fontsize=size, fontweight='bold')
    ax3.plot(R/10, np.divide(RT2, O1),  linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax3.plot(R/10, np.divide(PT2, opt2),  linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    ax4.set_title("Random (rho=2)", fontsize=size, fontweight='bold')
    ax4.plot(R/10, np.divide(RR2, O1), linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax4.plot(R/10, np.divide(PR2, opt2), linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    ax5.set_title("Trustworthy (rho=4)", fontsize=size, fontweight='bold')
    ax5.plot(R/10, np.divide(RT4, O2), linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax5.plot(R/10, np.divide(PT4, opt4), linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    ax6.set_title("Random (rho=4)",fontsize=size,fontweight='bold')
    ax6.plot(R/10, np.divide(RR4, O2), linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax6.plot(R/10, np.divide(PR4, opt4), linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    ax7.set_title("Trustworthy (rho=6)", fontsize=size, fontweight='bold')
    ax7.plot(R/10, np.divide(RT8, O3),  linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax7.plot(R/10, np.divide(PT8, opt8),  linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    ax8.set_title("Random (rho=6)",fontsize=size,fontweight='bold')
    ax8.plot(R/10, np.divide(RR8, O3),  linestyle='-',
             color='tab:purple', label='N-REFORM', linewidth=5)
    ax8.plot(R/10, np.divide(PR8, opt8),  linestyle='--',
             color='tab:green', label='N-RPTSC', linewidth=5)

    for ax in fig.get_axes():
        ax.label_outer()


    plt.xlim(0, 20)
    ax3.set_ylim([-0.5, 1])
    ax4.set_ylim([-0.5, 0.5])
    ax4.set_xticks([0, 10, 20])
    ax3.set_yticks([-0.5, 0, 0.5, 1])
    ax4.set_yticks([-0.5, 0, 0.5])

    plt.setp(ax3.get_yticklabels(), fontsize=size-2,
             fontweight="bold", horizontalalignment="right")
    plt.setp(ax4.get_yticklabels(), fontsize=size-2,
             fontweight="bold", horizontalalignment="right")
    plt.setp(ax4.get_xticklabels(), fontsize=size-2,
             fontweight="bold", horizontalalignment="right")
    plt.setp(ax6.get_xticklabels(), fontsize=size-2,
             fontweight="bold", horizontalalignment="right")
    plt.setp(ax8.get_xticklabels(), fontsize=size-2,
             fontweight="bold", horizontalalignment="right")

    labels = ["N-REFORM", "N-RPTSC"]
    marker = ["-", "--"]
    legend_properties = {'size':'14','weight': 'bold'}
    fig.legend(marker, labels=labels, ncol=2, bbox_to_anchor=(0.65, 1.0), prop=legend_properties)

    fig.text(0.5, 0.01, 'Rounds (x10)', ha='center',
             fontsize=size, fontweight='bold')
    fig.text(0.01, 0.5, 'Normailzed Reward', va='center',
             rotation='vertical', fontsize=size, fontweight='bold')
    plt.show()

def main():
    O2 = []
    RT2 = []
    PT2 = []
    RR2 = []
    PR2 = []
    O4 = []
    RT4 = []
    PT4 = []
    RR4 = []
    PR4 = []
    O8 = []
    RT8 = []
    PT8 = []
    RR8 = []
    PR8 = []

    # getting avg rewards over 200 rounds for rho = 2,4,6
    print("-------------------------------------------------------------------------------------")
    O2, RT2, PT2, RR2, PR2, O12 = get_rewards(2)
    print("-------------------------------------------------------------------------------------")
    O4, RT4, PT4, RR4, PR4, O14 = get_rewards(4)
    print("-------------------------------------------------------------------------------------")
    O8, RT8, PT8, RR8, PR8, O18 = get_rewards(6)
    print("-------------------------------------------------------------------------------------")

    # plotting the obtained rewards
    plots(O2, RT2, PT2, RR2, PR2, O4, RT4, PT4, RR4,
          PR4, O8, RT8, PT8, RR8, PR8, O12, O14, O18)
    print("-------------------------------------------------------------------------------------")
    print(O2)
    print(RT2)
    print(PT2)
    print(RR2)
    print(PR2)
    print(O4)
    print(RT4)
    print(PT4)
    print(RR4)
    print(PR4)
    print(O8)
    print(RT8)
    print(PT8)
    print(RR8)
    print(PR8)

if __name__ == "__main__":
    main()
