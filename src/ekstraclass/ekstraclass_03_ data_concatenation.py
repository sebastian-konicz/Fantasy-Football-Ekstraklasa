from pathlib import Path
import pandas as pd
import time
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # variables
    season = '2021_2022'
    round = 31
    # last season before break file
    season_prev = '2021_2022'
    round_final = 19

    # input files
    players_stats_prev_season_path = r'\data\raw\02_players_stats_{s}_round_{r}.csv'.format(s=season_prev, r=round_final)
    players_stats_curr_season_path = r'\data\raw\02_players_stats_{s}_round_{r}.csv'.format(s=season, r=round)

    # output files
    players_stats_path = r'\data\interim\round_{r}\03_players_concat_before_round_{r}.csv'.format(s=season, r=round)

    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[2])

    # loading file with data concerning previous season
    players_stats_prev = pd.read_csv(project_dir + players_stats_prev_season_path, delimiter=',')

    # loading file with data concerning current season
    players_stats_curr = pd.read_csv(project_dir + players_stats_curr_season_path, delimiter=',')

    # dropping duplicates
    players_stats_prev.drop_duplicates(keep='first', inplace=True)
    players_stats_curr.drop_duplicates(keep='first', inplace=True)

    # concatenating two dataframes
    players_stats = pd.concat([players_stats_prev, players_stats_curr])

    # sorting data
    players_stats.sort_values(by=['id', 'round'], inplace=True)

    # players current status
    players_status = players_stats_curr[players_stats_curr['round'] == round]

    # restricting dataframe
    players_status = players_status[['id', 'name', 'position', 'status', 'value']]

    # updating current status to concatenates dataframe
    players_stats = players_stats.merge(players_status, how='left', left_on=['name', 'id'], right_on=['name', 'id'], suffixes=['_old', '_new'])

    # renaming columns
    players_stats = players_stats.rename(columns={'status_new': 'status', 'value_new': 'value', 'position_new': 'position'})

    # dropping duplicates
    players_stats.drop_duplicates(subset=['name', 'id', 'round'], keep='first', inplace=True)

    # dropping unnecessary columns
    players_stats.drop(columns=['status_old', 'value_old', 'position_old'], inplace=True)

    # reshaping dataframe
    players_stats = players_stats[['id', 'name', 'position', 'value', 'club', 'club_abr', 'club_prev', 'country',
                                   'popularity',  'status', 'round', 'opponent', 'time', 'goals',
                                   'assists', 'own_goal', 'penalty', 'penalty_won', 'penalty_given', 'penalty_lost',
                                   'penalty_defended', 'in_stat', 'yellow_card', 'red_card', 'points']]
    # 'points_prev',
    # players_stats['status'].fillna(value="", inplace=True)
    #
    # players_stats['status'] = players_stats['status'].apply(lambda x: 'active' if x == "" else x)

    # saving dataframe
    players_stats.to_csv(project_dir + players_stats_path, index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()