from bs4 import BeautifulSoup
from pathlib import Path
import re
import pandas as pd
import time
from selenium import webdriver

PATH = r'C:\Users\kose9001\Desktop\JTM\chromedriver.exe'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])


    # gettig the page with stats for player
    driver = webdriver.Chrome(PATH)
    driver.get('https://ekstraklasa.org/rozgrywki/terminarz/ekstraklasa-4')

    # getting the site html
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')

    # shutting down selenium driver
    driver.quit()

    round_tables = site.find_all('table', class_="contestPart")

    # list of round dataframes
    round_list = []

    # loping through tables
    for table in round_tables:
        # round number
        pattern_round = re.compile("([0-9])+")
        round = table.find('thead').find('a').text
        round = re.search(pattern_round, round).group()

        score_table = table.find('tbody')
        rows = score_table.find_all('tr')

        # empty lists for scores
        col_round = []
        col_team_home =[]
        col_team_home_abr = []
        col_score_home = []
        col_result_home = []
        col_team_away = []
        col_team_away_abr = []
        col_score_away = []
        col_result_away = []

        for row in rows:
            # getting teams names and abreviations
            teams = row.find_all('div', class_="hidden-xs")
            teams_abr = row.find_all('div', class_="hidden-sm")

            team_home = teams[0].text
            team_home_abr = teams_abr[0].text

            team_away = teams[1].text
            team_away_abr = teams_abr[1].text

            try:
                score = row.find_all('td')[5].find_all('div')[0].find_all('div', class_="score")

                score_home = score[0].text
                score_away = score[1].text
            except IndexError:
                score_home = "-"
                score_away = "-"

            if score_home == "-":
                result_home = "-"
                result_away = "-"
            else:
                if score_home == score_away:
                    result_home = "D"
                    result_away = "D"
                elif score_home > score_away:
                    result_home = "W"
                    result_away = "L"
                else:
                    result_home = "L"
                    result_away = "W"

            # appending lists
            col_round.append(round)
            col_team_home.append(team_home)
            col_team_home_abr.append(team_home_abr)
            col_score_home.append(score_home)
            col_result_home.append(result_home)
            col_team_away.append(team_away)
            col_team_away_abr.append(team_away_abr)
            col_score_away.append(score_away)
            col_result_away.append(result_away)

        # zipping lists
        data_tuples = list(zip(col_round, col_team_home, col_team_home_abr, col_score_home, col_result_home,
                               col_team_away, col_team_away_abr, col_score_away, col_result_away))

        # creating dataframe
        round_results = pd.DataFrame(data_tuples, columns=["Round", "Team_home", "Team_home_abr", "Score_home", "Result_home",
                                                          "Team_away", "Team_away_abr", "Score_away", "Result_away"])
        # adding dataframe to list
        round_list.append(round_results)

    # concatenating dataframes
    rounds_results = pd.concat(round_list, axis=0, sort=False)


    # cleaning data
    letters_dictionary = {'ą': 'a', "ę": "e", "ć": "c", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z",
                          'Ą': 'A', "Ę": "E", "Ć": "C", "Ł": "L", "N": "N", "Ó": "O", "Ś": "S", "Ż": "Z", "Ź": "Z"}

    columns_list = ["Team_home", "Team_home_abr", "Team_away", "Team_away_abr"]

    # replacing special letters in columns:
    for special_letter, normal_letter in letters_dictionary.items():
        for column in columns_list:
            rounds_results[column] = rounds_results[column].apply(
                lambda value: value.replace(special_letter, normal_letter))

    print(rounds_results)
    # saving dataframe
    rounds_results.to_csv(project_dir + r'\data\raw\Rounds_results.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


