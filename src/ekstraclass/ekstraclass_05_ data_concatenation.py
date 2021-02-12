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

    # loading file with data concerning previous season
    players_stats_prev = pd.read_csv(project_dir + r'\data\raw\ekstraclass\02_players_stats_14_final_round_autumn.csv', delimiter=',')

    # loading file with data concerning current season
    players_stats_curr = pd.read_csv(project_dir + r'\data\raw\ekstraclass\02_players_stats_21_02_12_round_16.csv', delimiter=',')

    # concatenating two dataframes
    players_stats = pd.concat([players_stats_prev, players_stats_curr])

    # sorting data
    players_stats.sort_values(by=['id', 'round'], inplace=True)

    # players current status
    players_status = players_stats_curr[players_stats_curr['round'] == 15]

    # restricting dataframe
    players_status = players_status[['name', 'status', 'value']]

    # updating current status to concatenates dataframe
    players_stats = players_stats.merge(players_status, how='left', left_on='name', right_on='name', suffixes=['_old', '_new'])

    # renaming columns
    players_stats = players_stats.rename(columns={'status_new': 'status', 'value_new': 'value'})

    # dropping unnecessary columns
    players_stats.drop(columns=['status_old', 'value_old'], inplace=True)

    # reshaping dataframe
    players_stats = players_stats[['id', 'name', 'position', 'value', 'club', 'club_abr', 'club_prev', 'country',
                                   'popularity', 'points_prev', 'status', 'round', 'opponent', 'time', 'goals',
                                   'assists', 'own_goal', 'penalty', 'penalty_won', 'penalty_given', 'penalty_lost',
                                   'penalty_defended', 'in_stat', 'yellow_card', 'red_card', 'points']]

    # saving dataframe
    players_stats.to_csv(project_dir + r'\data\interim\ekstraclass\05_players_concat.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()