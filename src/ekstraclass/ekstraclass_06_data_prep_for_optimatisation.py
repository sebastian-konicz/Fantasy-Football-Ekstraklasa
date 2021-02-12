from pathlib import Path
import pandas as pd
import time
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[2])

    # loading file with data
    players_stats = pd.read_csv(project_dir + r'\data\interim\ekstraclass\05_players_concat.csv', delimiter=',')

    # restricting data to necessary columns
    players_stats = players_stats[['id', 'name', 'position', 'club', 'value', 'points', 'status']]

    # restricting data to active payers only
    players_stats = players_stats[players_stats["status"] == 'active']

    # changing text values to number values
    # club / team
    club_dictionary = {"Cracovia": 1, "Gornik Zabrze": 2, "Jagiellonia Bialystok": 3, "Legia Warszawa": 4,
                       "Lechia Gdansk": 5, "Lech Poznan": 6, "Piast Gliwice": 7, "Podbeskidzie Bielsko-Biala": 8,
                       "Pogon Szczecin": 9, "Rakow Czestochowa": 10,"Slask Wroclaw": 11, "PGE FKS Stal Mielec": 12,
                       "Warta Poznan": 13, "Wisla Krakow": 14, "Wisla Plock": 15, "Zaglebie Lubin": 16}

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
    position_dictionary = {" Bramkarz": 1, " Obronca": 2, " Pomocnik": 3, " Napastnik": 4}

    for position_name, position_no in position_dictionary.items():
        players_stats["position"] = players_stats.apply(
            lambda ps: position_no
            if ps["position"] == position_name
            else ps["position"], axis=1)

    players_stats_sum = pd.DataFrame(players_stats.groupby(['id', 'name', 'position', 'club', 'value'])['points'].sum()).reset_index()

    # time stamp
    today = dt.date.today()
    day = today.strftime("%d")
    month = today.strftime("%b").upper()
    year = today.strftime("%y")
    time_stamp = day + month + year

    # saving dataframe
    players_stats_sum.to_csv(project_dir + r'\data\interim\ekstraclass\06_players_sum_stats_{date}.csv'.format(date=time_stamp),
                          index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()