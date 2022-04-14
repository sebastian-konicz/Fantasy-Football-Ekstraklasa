from pathlib import Path
import src.ekstraclass.ekstraclass_05_team_optimatisation_no_transfers as team
import pandas as pd
import time
import datetime as dt
import pulp
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main(team_name, season, round, points_type, budget_now, sub_factor):

    round_prev = round - 1 # uwaga mogą się zmienic rundy pomiedzy sezonami 39 na 01

    # input files
    players_stats_sum_all_path = r'\data\interim\round_{r}\04_players_sum_stats_{s}_{t}_round_{r}.csv'.format(s=season, r=round, t=points_type)
    squad_old_dataframe_path = r'\data\final\squads\{tn}\{tn}_squad_{s}_round_{r}.csv'.format(tn=team_name, s=season, r=round_prev)

    # output files
    squad_new_dataframe_path = r'\data\final\squads\{tn}\{tn}_squad_{s}_round_{r}.csv'.format(tn=team_name, s=season, r=round)

    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[2])

    # loading file with data
    players_stats = pd.read_csv(project_dir + players_stats_sum_all_path, delimiter=',')
    squad = pd.read_csv(project_dir + squad_old_dataframe_path, delimiter=';')

    print(players_stats.tail())
    print(squad)

    # restricting squad dataframe
    squad = squad[['id', 'name', 'position', 'club', 'value', 'points']]

    # currend squad
    # allocating old squad on current players array
    squad_player_id_list = squad['id'].to_list()

    def index_creation(players_stats):
        index_list = []

        for id in squad_player_id_list:
            try:
                index = int(players_stats[players_stats['id'] == id].index[0])
                index_list.append(index)
            except IndexError:
                print('brak zawodnika o id = ', id)
                index_list.append("missing")

        return index_list

    index_list = index_creation(players_stats)

    # creating dictionary with id's and index
    squad_dict = dict(zip(squad_player_id_list, index_list))

    # missing players in players_stats - probably due to injury or transfer etc.
    missing_players_list = []
    for key, value in squad_dict.items():
        if value == "missing":
            print(f'brakujące id to {key}')
            missing_player_id = key
            missing_players_list.append(missing_player_id)
        else:
            pass

    print(missing_players_list)

    # gettign dataframes
    missing_df_list = []
    for missing in missing_players_list:
        missing_df = squad[squad['id'] == missing]
        missing_df.reset_index(drop=True, inplace=True)
        missing_df.at[0, 'points'] = 0
        print(missing_df)
        missing_df_list.append(missing_df)

    # concatenating missing players
    if len(missing_df_list) != 0:
        concat_df = pd.concat(missing_df_list, axis=0, sort=False)

        # adding missing players to players stats dataframe - added at the bottom of dataframe
        players_stats = pd.concat([players_stats, concat_df], axis=0, sort=False)
        print(players_stats.tail(5))

        # reseting index - new values at the bottom of the index
        players_stats.reset_index(inplace=True, drop=True)
    else:
        pass



    # once again getting index list (hopefully the last) - room for improvment - dedicated function
    index_list = index_creation(players_stats)

    # index_list = [208, 197, 127, 219, 162, 198, 319, 462, 121, 221, 406, 210, 289, 169]
    current_squad_indices = index_list
    # current_squad_indices = team.main()

    # geting columns with values
    expected_scores = players_stats['points']
    buy_prices = players_stats['value']
    sell_prices = players_stats['value']
    positions = players_stats['position']
    clubs = players_stats['club']
    names = players_stats['name']
    player_id = players_stats['id']
    num_players = len(players_stats['points'])

    opt = TransferOptimiser(expected_scores, buy_prices, sell_prices, positions, clubs)

    transfer_in_decisions, transfer_out_decisions, starters, sub_decisions, captain_decisions, current_squad_decisions = opt.solve(
        current_squad_indices, budget_now=budget_now, sub_factor=sub_factor)

    print('### CURRENT_SQUAD ###')
    for i in range(num_players):
        if current_squad_decisions[i] == 1:
            print("{}, {}, {}, {}, {}".format(i, names[i], expected_scores[i], buy_prices[i], player_id[i]))

    print('\n### TRANSFERS ###')
    for i in range(num_players):
        if transfer_in_decisions[i].value() == 1:
            print("Transferred in: {} {} {}".format(names[i], buy_prices[i], expected_scores[i]))
        if transfer_out_decisions[i].value() == 1:
            print("Transferred out: {} {} {}".format(names[i], sell_prices[i], expected_scores[i]))

    print('\n### CAPTAIN ###')
    for i in range(num_players):
        if captain_decisions[i].value() == 1:
            print("Captain decision: {} {} {}".format(names[i], sell_prices[i], expected_scores[i]))

    # empty lists for saving results
    id_list = []
    name_list = []
    position_list = []
    club_list = []
    value_list = []
    points_list = []
    type_list = []
    captain_list = []

    print("")
    print("### New first team ###")
    for i in range(num_players):
        if (starters[i].value() != 0) & (captain_decisions[i].value() == 0):
            print(names[i], ",", expected_scores[i], ",", player_id[i])
            # values for saving
            captain = 'no'
            type = 'first'
            id_list.append(player_id[i])
            name_list.append(names[i])
            position_list.append(positions[i])
            club_list.append(clubs[i])
            value_list.append(buy_prices[i])
            points_list.append(expected_scores[i])
            type_list.append(type)
            captain_list.append(captain)

        if (starters[i].value() != 0) & (captain_decisions[i].value() == 1):
            print(names[i],",", expected_scores[i],",", buy_prices[i],",", player_id[i])
            # values for saving
            captain = 'yes'
            type = 'first'
            id_list.append(player_id[i])
            name_list.append(names[i])
            position_list.append(positions[i])
            club_list.append(clubs[i])
            value_list.append(buy_prices[i])
            points_list.append(expected_scores[i])
            type_list.append(type)
            captain_list.append(captain)

    print()
    print(("### New subs ###"))
    # print results
    for i in range(players_stats.shape[0]):
        if sub_decisions[i].value() == 1:
            print(names[i],",", expected_scores[i],",", buy_prices[i],",", player_id[i])
            # values for saving
            captain = 'no'
            type = 'sub'
            id_list.append(player_id[i])
            name_list.append(names[i])
            position_list.append(positions[i])
            club_list.append(clubs[i])
            value_list.append(buy_prices[i])
            points_list.append(expected_scores[i])
            type_list.append(type)
            captain_list.append(captain)

    # saving results
    # zipping lists
    data_tuples = list(zip(id_list, name_list, position_list, club_list, value_list, points_list, type_list, captain_list))

    # creating dataframe
    team_dataframe = pd.DataFrame(data_tuples, columns=["id", "name", "position", "club", "value", "points", "type", "captain"])

    team_dataframe.sort_values(['type', 'position', 'club'], inplace=True)

    # saving dataframe
    team_dataframe.to_csv(project_dir + squad_new_dataframe_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

position_data = {
    "gk": {"position_id": 1, "min_starters": 1, "max_starters": 1, "num_total": 2},
    "df": {"position_id": 2, "min_starters": 3, "max_starters": 5, "num_total": 5},
    "mf": {"position_id": 3, "min_starters": 3, "max_starters": 5, "num_total": 5},
    "fw": {"position_id": 4, "min_starters": 1, "max_starters": 3, "num_total": 3},
}

def get_decision_array(name, length):
    return np.array([
        pulp.LpVariable("{}_{}".format(name, i), lowBound=0, upBound=1, cat='Integer')
        for i in range(length)
    ])

class TransferOptimiser:
    def __init__(self, expected_scores, buy_prices, sell_prices, positions, clubs):
        self.expected_scores = expected_scores
        self.buy_prices = buy_prices
        self.sell_prices = sell_prices
        self.positions = positions
        self.clubs = clubs
        self.num_players = len(buy_prices)

    def instantiate_decision_arrays(self):
        # we will make transfers in and out of the squad, and then pick subs and captains from that squad
        transfer_in_decisions_free = get_decision_array("transfer_in_free", self.num_players)
        transfer_in_decisions_paid = get_decision_array("transfer_in_paid", self.num_players)
        transfer_out_decisions = get_decision_array("transfer_out_paid", self.num_players)
        # total transfers in will be useful later
        transfer_in_decisions = transfer_in_decisions_free + transfer_in_decisions_paid

        sub_decisions = get_decision_array("subs", self.num_players)
        captain_decisions = get_decision_array("captain", self.num_players)
        return transfer_in_decisions_free, transfer_in_decisions_paid, transfer_out_decisions, transfer_in_decisions, sub_decisions, captain_decisions

    def encode_player_indices(self, indices):
        decisions = np.zeros(self.num_players)
        # tu prawdopodobnie potrzebna jest zmiana dot id zawodników - ten sam scope
        decisions[indices] = 1
        return decisions

    # constraints on transfers
    #     only one free transfer allowed per week
    #     the transfer budget cannot drop below zero
    def apply_transfer_constraints(self, model, transfer_in_decisions_free, transfer_in_decisions,
                                   transfer_out_decisions, budget_now):
        # only 2 free transfers
        model += sum(transfer_in_decisions_free) <= 2

        # budget constraint
        transfer_in_cost = sum(transfer_in_decisions * self.buy_prices)
        transfer_out_cost = sum(transfer_out_decisions * self.sell_prices)
        budget_next_week = budget_now + transfer_out_cost - transfer_in_cost
        model += budget_next_week >= 0


    def solve(self, current_squad_indices, budget_now, sub_factor):
        current_squad_decisions = self.encode_player_indices(current_squad_indices)

        model = pulp.LpProblem("Transfer optimisation", pulp.LpMaximize)
        transfer_in_decisions_free, transfer_in_decisions_paid, transfer_out_decisions, transfer_in_decisions, sub_decisions, captain_decisions = self.instantiate_decision_arrays()

        # calculate new team from current team + transfers
        next_week_squad = current_squad_decisions + transfer_in_decisions - transfer_out_decisions
        starters = next_week_squad - sub_decisions

        # points penalty for additional transfers - 3 points
        transfer_penalty = sum(transfer_in_decisions_paid) * 3

        self.apply_transfer_constraints(model, transfer_in_decisions_free, transfer_in_decisions,
                                        transfer_out_decisions, budget_now)
        self.apply_formation_constraints(model, squad=next_week_squad, starters=starters,
                                         subs=sub_decisions, captains=captain_decisions)

        # objective function:
        model += self.get_objective(starters, sub_decisions, captain_decisions, sub_factor, transfer_penalty, self.expected_scores), "Objective"
        status = model.solve()

        print("Solver status: {}".format(status))

        return transfer_in_decisions, transfer_out_decisions, starters, sub_decisions, captain_decisions, current_squad_decisions

    def get_objective(self, starters, subs, captains, sub_factor, transfer_penalty, scores):
        starter_points = sum(starters * scores)
        sub_points = sum(subs * scores) * sub_factor
        captain_points = sum(captains * scores)
        return starter_points + sub_points + captain_points - transfer_penalty

    def apply_formation_constraints(self, model, squad, starters, subs, captains):
        for position, data in position_data.items():
            # formation constraints
            model += sum(starter for starter, position in zip(starters, self.positions) if position == data["position_id"]) >= data["min_starters"]
            model += sum(starter for starter, position in zip(starters, self.positions) if position == data["position_id"]) <= data["max_starters"]
            model += sum(selected for selected, position in zip(squad, self.positions) if position == data["position_id"]) == data["num_total"]

        # club constraint
        for club_id in np.unique(self.clubs):
            model += sum(selected for selected, club in zip(squad, self.clubs) if club == club_id) <= 3  # max 3 players

        # total team size
        model += sum(starters) == 11
        model += sum(squad) == 15
        model += sum(captains) == 1

        for i in range(self.num_players):
            model += (starters[i] - captains[i]) >= 0  # captain must also be on team
            model += (starters[i] + subs[i]) <= 1  # subs must not be on team


def get_decision_array_2d(name, n_players, n_weeks):
    return np.array([[
        pulp.LpVariable("{}_{}_w{}".format(name, i, j), lowBound=0, upBound=1, cat='Integer')
        for i in range(n_players)
    ] for j in range(n_weeks)])


class MultiHorizonTransferOptimiser(TransferOptimiser):
    """We now plan transfer decisions over multiple weeks. This means we need a 2d array of expected
    scores (n_players x n_weeks) and 2d arrays of decision variables"""
    def __init__(self, expected_scores, buy_prices, sell_prices, positions, clubs,
                 n_weeks):
        super().__init__(expected_scores, buy_prices, sell_prices, positions, clubs)
        self.num_weeks = n_weeks

    def instantiate_decision_arrays(self):
        # we will make transfers in and out of the squad, and then pick subs and captains from that squad
        transfer_in_decisions_free = get_decision_array_2d("transfer_in_free", self.num_players, self.num_weeks)
        transfer_in_decisions_paid = get_decision_array_2d("transfer_in_paid", self.num_players, self.num_weeks)
        transfer_out_decisions = get_decision_array_2d("transfer_out_paid", self.num_players, self.num_weeks)
        # total transfers in will be useful later
        transfer_in_decisions = [a + b for a, b in zip(transfer_in_decisions_free, transfer_in_decisions_paid)]

        sub_decisions = get_decision_array_2d("subs", self.num_players, self.num_weeks)
        captain_decisions = get_decision_array_2d("captain", self.num_players, self.num_weeks)
        return transfer_in_decisions_free, transfer_in_decisions_paid, transfer_out_decisions, transfer_in_decisions, sub_decisions, captain_decisions

    def solve(self, current_squad_indices, budget_now, sub_factor):
        current_squad_decisions = self.encode_player_indices(current_squad_indices)
        model = pulp.LpProblem("Transfer optimisation", pulp.LpMaximize)
        (transfer_in_decisions_free_all, transfer_in_decisions_paid_all, transfer_out_decisions_all,
         transfer_in_decisions_all, sub_decisions_all, captain_decisions_all) = self.instantiate_decision_arrays()

        total_points = 0
        for w in range(self.num_weeks):
            transfer_in_decisions_free = transfer_in_decisions_free_all[w]
            transfer_in_decisions_paid = transfer_in_decisions_paid_all[w]
            transfer_out_decisions = transfer_out_decisions_all[w]
            transfer_in_decisions = transfer_in_decisions_all[w]
            sub_decisions = sub_decisions_all[w]
            captain_decisions = captain_decisions_all[w]

            # calculate new team from current team + transfers
            next_week_squad = current_squad_decisions + transfer_in_decisions - transfer_out_decisions
            starters = next_week_squad - sub_decisions

            # points penalty for additional transfers
            transfer_penalty = sum(transfer_in_decisions_paid) * 4

            self.apply_transfer_constraints(model, transfer_in_decisions_free, transfer_in_decisions,
                                            transfer_out_decisions, budget_now)
            self.apply_formation_constraints(model, squad=next_week_squad, starters=starters,
                                             subs=sub_decisions, captains=captain_decisions)

            # objective function:
            total_points += self.get_objective(starters, sub_decisions, captain_decisions, sub_factor, transfer_penalty, self.expected_scores[w])
            current_squad_decisions = next_week_squad

        model += total_points, "Objective"
        model.solve()

        return transfer_in_decisions_all, transfer_out_decisions_all, sub_decisions_all, sub_decisions_all, captain_decisions_all

if __name__ == "__main__":
    # # variables
    team_name = 'algolrytm_05'
    season = '2021_2022'
    round = 29
    points_type = '15'
    budget_now = 0.3
    sub_factor = 0.5
    main(team_name, season, round, points_type, budget_now, sub_factor)