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
    players_stats = pd.read_csv(project_dir + r'\data\raw\first_league\02_players_stats_21_02_12.csv', delimiter=',')

    # restricting data to necessary columns
    players_stats = players_stats[['id', 'name', 'position', 'club', 'value', 'points', 'status']]

    # changing text values to number values
    # club / team
    club_dictionary = {"Apklan Resovia": 1, "Arka Gdynia": 2, "Bruk-Bet Termalica Nieciecza": 3, "Chrobry Glogow": 4,
                       "GKS Belchatow": 5, "GKS Jastrzebie ": 6, "GKS Tychy": 7, "Gornik Leczna": 8, "Korona Kielce": 9,
                       "LKS Lodz": 10, "Miedz Legnica": 11, "Odra Opole": 12, "Puszcza Niepolomice": 13,
                       "Radomiak Radom": 14, "Sandecja Nowy Sacz": 15, "Stomil Olsztyn": 16, "Widzew Lodz": 17,
                       "Zaglebie Sosnowiec": 18}

    for club_name, club_no in club_dictionary.items():
        players_stats["club"] = players_stats.apply(
            lambda ps: club_no
            if ps["club"] == club_name
            else ps["club"], axis=1)

    # changing the value
    players_stats["value"] = players_stats.apply(
        lambda ps: ((int(ps['value'].replace(',', ''))) / 100)
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

    # loading file with data
    players_value = pd.read_csv(project_dir + r'\data\raw\first_league\02_players_stats_21_02_25.csv', sep=',')

    # getting new values for the players
    players_value = players_value[players_value['round'] == 18]
    players_value = players_value[['id', 'name', 'position', 'club', 'value', 'points', 'status']].copy()

    # changing text values to number values
    # club / team
    for club_name, club_no in club_dictionary.items():
        players_value["club"] = players_value.apply(
            lambda pv: club_no
            if pv["club"] == club_name
            else pv["club"], axis=1)

    # changing the value
    players_value["value"] = players_value.apply(
        lambda pv: (int(pv['value'].replace(',', ''))) / 100
        if pv['value'].find(",") != -1
        else int(pv['value']), axis=1)

    # position
    position_dictionary = {" Bramkarz": 1, " Obronca": 2, " Pomocnik": 3, " Napastnik": 4}

    for position_name, position_no in position_dictionary.items():
        players_value["position"] = players_value.apply(
            lambda pv: position_no
            if pv["position"] == position_name
            else pv["position"], axis=1)

    players_value.to_csv(
        project_dir + r'\data\interim\first_league\08_players_new_values.csv', index=False, encoding='UTF-8')

    players_merged = players_stats_sum.merge(players_value, how='right', left_on='id', right_on='id', suffixes=['_old', '_new'])

    players_merged.drop_duplicates(keep='first', inplace=True)

    players_merged['points_new'] = players_merged.apply(
        lambda pm: pm['points_old']
        if pm['points_old'] != ''
        else pm['points_new'], axis=1)

    players_merged['points_new'].fillna(value=0, axis=0, inplace=True)

    # restricting dataframe to only necessary columns
    players_merged = players_merged[['id', 'name_new', 'position_new', 'club_new', 'value_new', 'points_new', 'status']]

    # renaming columns
    players_merged = players_merged.rename(columns={'name_new': 'name', 'position_new': 'position', 'club_new': 'club',
                                                    'value_new': 'value', 'points_new': 'points'})

    # restricting data to active payers only
    players_merged = players_merged[players_merged["status"] == 'active']


    # time stamp
    today = dt.date.today()
    day = today.strftime("%d")
    month = today.strftime("%b").upper()
    year = today.strftime("%y")
    time_stamp = day + month + year

    # saving dataframe
    players_merged.to_csv(
        project_dir + r'\data\interim\first_league\08_players_updated_values_{date}.csv'.format(date=time_stamp),
        index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()