import src.ekstraclass.ekstraclass_00_variables as var
from pathlib import Path
import pandas as pd
import time
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # variables
    season = '2021_2022'
    round = 22
    date = 'autumn'

    # input files
    players_stats_path = r'\data\interim\round_{r}\03_players_concat_before_round_{r}.csv'.format(s=season, r=round)
    # players_stats_path = r'\data\interim\ekstraclass\05_players_concat_before_round_20.csv'

    # output files
    players_stats_sum_all_path = r'\data\interim\round_{r}\04_players_sum_stats_{s}_all_round_{r}.csv'.format(s=season, r=round)
    players_stats_sum_5_rounds_path = r'\data\interim\round_{r}\04_players_sum_stats_{s}_05_round_{r}.csv'.format(s=season, r=round)
    players_stats_sum_10_rounds_path = r'\data\interim\round_{r}\04_players_sum_stats_{s}_10_round_{r}.csv'.format(s=season, r=round)
    players_stats_sum_15_rounds_path = r'\data\interim\round_{r}\04_players_sum_stats_{s}_15_round_{r}.csv'.format(s=season, r=round)

    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[2])

    # loading file with data
    players_stats = pd.read_csv(project_dir + players_stats_path, delimiter=',')

    # # loading file with data concerning current season
    # players_stats = pd.read_csv(project_dir + r'\data\raw\ekstraclass\02_players_stats_22_01_24_round_19_autumn_2021.csv',
    #                                  delimiter=',')

    # # restricting dataframe to certina number of rounds
    # players_stats = players_stats[players_stats['round'] <= round]

    # restricting data to necessary columns
    players_stats = players_stats[['id', 'name', 'position', 'club', 'value', 'points', 'status', 'round']]

    # restricting data to active payers only
    players_stats = players_stats[players_stats["status"] == 'active']

    # changing text values to number values
    # club / team
    club_dictionary = {"Bruk-Bet Termalica Nieciecza": 1,
                       "Cracovia": 2,
                       "Gornik Leczna": 3,
                       "Gornik Zabrze": 4,
                       "Jagiellonia Bialystok": 5,
                       "Lech Poznan": 6,
                       "Lechia Gdansk": 7,
                       "Legia Warszawa": 8,
                       "PGE FKS Stal Mielec": 9,
                       "Piast Gliwice": 10,
                       "Pogon Szczecin": 11,
                       "Radomiak Radom": 12,
                       "Rakow Czestochowa": 13,
                       "Slask Wroclaw": 14,
                       "Warta Poznan": 15,
                       "Wisla Krakow": 16,
                       "Wisla Plock": 17,
                       "Zaglebie Lubin": 18}

    for club_name, club_no in club_dictionary.items():
        players_stats["club"] = players_stats.apply(
            lambda ps: club_no
            if ps["club"] == club_name
            else ps["club"], axis=1)

    # changing the value
    players_stats["value"] = players_stats.apply(
        lambda ps: (int(ps['value'].replace(',', ''))) / 100
        if ps['value'].find(",") != -1
        else int(ps['value']), axis=1)

    # position
    position_dictionary = {"Bramkarz": 1, "Obronca": 2, "Pomocnik": 3, "Napastnik": 4}

    for position_name, position_no in position_dictionary.items():
        players_stats["position"] = players_stats.apply(
            lambda ps: position_no
            if ps["position"] == position_name
            else ps["position"], axis=1)

    players_stats_sum_all = pd.DataFrame(
        players_stats.groupby(['id', 'name', 'position', 'club', 'value'])['points'].sum()).reset_index()

    # saving dataframe
    players_stats_sum_all.to_csv(project_dir + players_stats_sum_all_path, index=False, encoding='UTF-8')

    # moving averages
    behind_5_rounds = round - 5
    behind_10_rounds = round - 10
    behind_15_rounds = round - 15

    # 5 rounds back
    players_stats_5_rounds = players_stats[players_stats['round'] > behind_5_rounds].copy()
    players_stats_sum_5_rounds = pd.DataFrame(
        players_stats_5_rounds.groupby(['id', 'name', 'position', 'club', 'value'])['points'].sum()).reset_index()

    players_stats_sum_5_rounds.to_csv(project_dir + players_stats_sum_5_rounds_path, index=False, encoding='UTF-8')

    # 10 rounds back
    players_stats_10_rounds = players_stats[players_stats['round'] > behind_10_rounds].copy()
    players_stats_sum_10_rounds = pd.DataFrame(
        players_stats_10_rounds.groupby(['id', 'name', 'position', 'club', 'value'])['points'].sum()).reset_index()

    players_stats_sum_10_rounds.to_csv(project_dir + players_stats_sum_10_rounds_path, index=False, encoding='UTF-8')

    # 15 rounds back
    players_stats_15_rounds = players_stats[players_stats['round'] > behind_15_rounds].copy()
    players_stats_sum_15_rounds = pd.DataFrame(
        players_stats_15_rounds.groupby(['id', 'name', 'position', 'club', 'value'])['points'].sum()).reset_index()

    players_stats_sum_15_rounds.to_csv(project_dir + players_stats_sum_15_rounds_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()