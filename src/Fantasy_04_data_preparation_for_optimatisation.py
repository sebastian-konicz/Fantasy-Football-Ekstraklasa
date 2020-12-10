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
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading file with data
    players_stats = pd.read_csv(project_dir + r'\data\raw\Players_stats_10DEC20.csv', delimiter=';')

    # restricting data to necessary columns
    players_stats = players_stats[['name', 'position', 'value']]

    print(players_stats.columns)
    print(players_stats.columns)

    # time stamp
    today = dt.date.today()
    day = today.strftime("%d")
    month = today.strftime("%b").upper()
    year = today.strftime("%y")
    time_stamp = day + month + year

    # saving dataframe
    # rounds_results.to_csv(project_dir + r'\data\raw\Rounds_results_{date}.csv'.format(date=time_stamp),
    #                       index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()