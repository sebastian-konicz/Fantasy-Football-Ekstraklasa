from pathlib import Path
import pandas as pd
import time
import datetime as dt
import pulp
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading file with data
    players_stats = pd.read_csv(project_dir + r'\data\interim\Players_sum_stats_11DEC20.csv', delimiter=',')

    print(players_stats.dtypes)

    # geting columns with values
    expected_scores = players_stats['points']
    prices = players_stats['value']
    positions = players_stats['position']
    clubs = players_stats['club']
    names = players_stats['name']

    decisions, captain_decisions, sub_decisions = select_team(expected_scores.values, prices.values, positions.values,
                                                              clubs.values, sub_factor=0.2)

    # print results
    for i in range(players_stats.shape[0]):
        if decisions[i].value() != 0:
            print(names[i], expected_scores[i], prices[i])
    print()
    print("Subs:")
    # print results
    for i in range(players_stats.shape[0]):
        if sub_decisions[i].value() == 1:
            print(names[i], expected_scores[i], prices[i])

    print()
    print("Captain:")
    # print results
    for i in range(players_stats.shape[0]):
        if captain_decisions[i].value() == 1:
            print(names[i], expected_scores[i], prices[i])

    # time stamp
    today = dt.date.today()
    day = today.strftime("%d")
    month = today.strftime("%b").upper()
    year = today.strftime("%y")
    time_stamp = day + month + year

    # # saving dataframe
    # players_stats_sum.to_csv(project_dir + r'\data\interim\Players_sum_stats_{date}.csv'.format(date=time_stamp),
    #                       index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')


def select_team(expected_scores, prices, positions, clubs, total_budget=30, sub_factor=0.2):
    num_players = len(expected_scores)
    model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)
    decisions = [
        pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]
    captain_decisions = [
        pulp.LpVariable("y{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]
    sub_decisions = [
        pulp.LpVariable("z{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]

    # objective function:
    model += sum((captain_decisions[i] + decisions[i] + sub_decisions[i] * sub_factor) * expected_scores[i]
                 for i in range(num_players)), "Objective"

    # cost constraint
    model += sum(
        (decisions[i] + sub_decisions[i]) * prices[i] for i in range(num_players)) <= total_budget  # total cost

    # position constraints
    # 1 starting goalkeeper
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 1) == 1
    # 2 total goalkeepers
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 1) == 2

    # 3-5 starting defenders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 2) >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 2) <= 5
    # 5 total defenders
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 2) == 5

    # 3-5 starting midfielders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 3) >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 3) <= 5
    # 5 total midfielders
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 3) == 5

    # 1-3 starting attackers
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 4) >= 1
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 4) <= 3
    # 3 total attackers
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 4) == 3

    # club constraint
    for club_id in np.unique(clubs):
        model += sum(
            decisions[i] + sub_decisions[i] for i in range(num_players) if clubs[i] == club_id) <= 3  # max 3 players

    model += sum(decisions) == 11  # total team size
    model += sum(captain_decisions) == 1  # 1 captain

    for i in range(num_players):
        model += (decisions[i] - captain_decisions[i]) >= 0  # captain must also be on team
        model += (decisions[i] + sub_decisions[i]) <= 1  # subs must not be on team

    model.solve()
    print("Total expected score = {}".format(model.objective.value()))

    return decisions, captain_decisions, sub_decisions

if __name__ == "__main__":
    main()