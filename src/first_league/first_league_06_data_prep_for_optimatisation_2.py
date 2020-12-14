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
    players_stats = pd.read_csv(project_dir + r'\data\raw\first_league\03_players_stats_hist_13DEC20.csv', delimiter=',')

    # restricting data to necessary columns
    players_stats = players_stats[['id', 'name', 'position', 'club', 'value', 'points', 'season']]

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

    players_stats_sum = players_stats[players_stats['season'] == '2019/20 - wiosna']

    # time stamp
    today = dt.date.today()
    day = today.strftime("%d")
    month = today.strftime("%b").upper()
    year = today.strftime("%y")
    time_stamp = day + month + year

    # saving dataframe
    players_stats_sum.to_csv(project_dir + r'\data\interim\first_league\06_players_sum_stats_hist_{date}.csv'.format(date=time_stamp),
                             index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()