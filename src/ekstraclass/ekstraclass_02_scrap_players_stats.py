import src.ekstraclass.ekstraclass_00_variables as var
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import time
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    # loading file with links
    # links_df = pd.read_csv(path + r'\data\raw\ekstraclass\01_players_links_{date}.csv'.format(date=var.time_stamp),
    #                        delimiter=',')
    links_df = pd.read_csv(path + r'\data\raw\ekstraclass\01_players_links_21_03_05.csv', delimiter=',')

    # creating list with links
    link_list = links_df["link"].tolist()

    # empty list with players dataframes
    players_stats_dataframes = []

    # looping throgu links
    for link in link_list:
        # gettig the page with stats for player
        driver = webdriver.Chrome(var.chrome_driver)
        driver.get(link)

        # getting the site html
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')

        # shutting down selenium driver
        driver.quit()

        # PLAYER INFO
        # getting elements with players info
        player_info_1 = site.find_all('h2')
        player_info_2 = site.find_all('h5', class_='mb-none')

        # general info about player
        player_id = link[39:]
        player_name = player_info_1[1].text
        print(player_name)
        player_club = player_info_1[0].text
        player_club_abr = ""
        player_position = site.find('h6').text

        # players value
        pattern_value = re.compile("([0-9]\.[0-9]\w)+")
        print(player_info_2)
        player_value = player_info_2[0].text
        player_value = re.search(pattern_value, player_value).group()

        # players popularity
        pattern_popularity = re.compile("([0-9])+")
        player_popularity = player_info_2[1].text
        player_popularity = re.search(pattern_popularity, player_popularity).group()

        # players country
        player_country = player_info_2[2].text
        player_country = player_country[6:]

        # players country
        player_club_prev = player_info_2[3].text
        player_club_prev = player_club_prev[16:]

        # previous edition points
        player_points_prev = player_info_2[4].text
        player_points_prev = player_points_prev[28:]

        # player status
        player_status = site.find('div', class_='col-sm-8')
        player_status = player_status.find('div', class_='mb-sm')
        pattern_status = re.compile("([A-Za-z])\w+")
        if player_status == None:
            player_status = "active"
        else:
            player_status = player_status.text
            player_status = player_status.replace(" ", "")
            player_status = player_status.replace("\n", "")[7:]

        # TABLE DATA
        table_body = site.find('tbody')
        table_rows = table_body.find_all('tr')

        # empty lists
        col_id = []
        col_name = []
        col_position = []
        col_value = []
        col_club = []
        col_club_abr = []
        col_club_prev = []
        col_status = []
        col_country = []
        col_popularity = []
        col_points_prev = []
        col_round = []
        col_opponent = []
        col_time = []
        col_goals = []
        col_assists = []
        col_own_goal = []
        col_penalty = []
        col_penalty_won = []
        col_penalty_given = []
        col_penalty_lost = []
        col_penalty_defend = []
        col_instat = []
        col_yellow = []
        col_red = []
        col_points = []

        # looping through rows in table
        for row in table_rows:
            # findin all columns
            col = row.find_all('td')
            if len(col) == 15:
                # reg-ex patterns
                pattern_lettes = re.compile("([A-Za-z])\w+")
                pattern_numbers = re.compile("([0-9])+")
                pattern_numbers_neg = re.compile("(\-)([0-9])+")

                # appending columns with general info about player
                col_id.append(player_id)
                col_name.append(player_name)
                col_position.append(player_position)
                col_value.append(player_value)
                col_club.append(player_club)
                col_club_abr.append(player_club_abr)
                col_club_prev.append(player_club_prev)
                col_country.append(player_country)
                col_popularity.append(player_popularity)
                col_points_prev.append(player_points_prev)
                col_status.append(player_status)

                # getting text from columns and appending lists
                round = col[0].text
                round = re.search(pattern_numbers, round).group()
                col_round.append(round)

                opponent = col[1].text
                opponent = pattern_lettes.search(opponent).group(0)
                col_opponent.append(opponent)

                gametime = col[2].text
                gametime = re.search(pattern_numbers, gametime).group()
                col_time.append(gametime)

                goals = col[3].text
                goals = re.search(pattern_numbers, goals).group()
                col_goals.append(goals)

                assists = col[4].text
                assists = re.search(pattern_numbers, assists).group()
                col_assists.append(assists)

                own_goal = col[5].text
                own_goal = re.search(pattern_numbers, own_goal).group()
                col_own_goal.append(own_goal)

                penalty = col[6].text
                penalty = re.search(pattern_numbers, penalty).group()
                col_penalty.append(penalty)

                penalty_won = col[7].text
                penalty_won = re.search(pattern_numbers, penalty_won).group()
                col_penalty_won.append(penalty_won)

                penalty_given = col[8].text
                penalty_given = re.search(pattern_numbers, penalty_given).group()
                col_penalty_given.append(penalty_given)

                penalty_lost = col[9].text
                penalty_lost = re.search(pattern_numbers, penalty_lost).group()
                col_penalty_lost.append(penalty_lost)

                penalty_defend = col[10].text
                penalty_defend = re.search(pattern_numbers, penalty_defend).group()
                col_penalty_defend.append(penalty_defend)

                instat = col[11].text
                instat = instat.replace('\n', '')
                # instat = re.search(pattern_numbers, instat).group()
                col_instat.append(instat)

                yellow = col[12].text
                yellow = re.search(pattern_numbers, yellow).group()
                col_yellow.append(yellow)

                red = col[13].text
                red = re.search(pattern_numbers, red).group()
                col_red.append(red)

                points = col[14].text
                # catching negative points
                try:
                    points = re.search(pattern_numbers_neg, points).group()
                except AttributeError:
                    points = re.search(pattern_numbers, points).group()
                col_points.append(points)

            else:
                pass

        # zipping lists
        data_tuples = list(zip(col_id, col_name, col_position, col_value, col_club, col_club_abr, col_club_prev,
                               col_country, col_popularity, col_points_prev, col_status, col_round, col_opponent,
                               col_time, col_goals, col_assists, col_own_goal, col_penalty, col_penalty_won,
                               col_penalty_given, col_penalty_lost, col_penalty_defend, col_instat, col_yellow,
                               col_red, col_points))


        # creating dataframe
        player_stats = pd.DataFrame(data_tuples, columns=["id", "name", "position", "value", "club", "club_abr",
                                                          "club_prev", "country", "popularity", "points_prev", "status",
                                                          "round", "opponent", "time", "goals", "assists", "own_goal",
                                                          "penalty", "penalty_won", "penalty_given", "penalty_lost",
                                                          "penalty_defended", "in_stat", "yellow_card", "red_card", "points"])

        # adding dataframe to list
        players_stats_dataframes.append(player_stats)

    # concatenating dataframes
    players_stats = pd.concat(players_stats_dataframes, axis=0, sort=False)

    # cleaning data
    # getting corect value (replacing "." in the nymber with ",")
    players_stats["value"] = players_stats["value"].apply(lambda value: value.replace(".", ","))

    # repairng opponent abbreviation
    players_stats["opponent"] = players_stats["opponent"].apply(lambda value: "SLA" if value == "LA" else value)

    letters_dictionary = {'ą': 'a', "ę": "e", "ć": "c", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z",
                          'Ą': 'A', "Ę": "E", "Ć": "C", "Ł": "L", "N": "N", "Ó": "O", "Ś": "S", "Ż": "Z", "Ź": "Z",
                          "á": "a", "Á": "A", "â": "a", "Â": "A", "ă": "a", "Ă": "A", "č": "c", "Č": "C", "đ": "d",
                          "Đ": "D", "é": "e", "É": "E", "í": "i", "Í": "I", "ľ": "l", "Ľ": "L", "ñ": "n", "Ñ": "N",
                          "ø": "o", "Ø": "O", "ö": "o", "Ö": "O", "ő": "o", "Ő": "O", "š": "s", "Š": "S", "ť": "t",
                          "Ť": "T", "ú": "u", "Ú": "U", "ý": "y", "Ý": "Y", "ž": "z", "Ž": "Z"}

    columns_list = ["name", "position", "club", "club_prev", "country", "opponent"]

    # replacing special letters in columns:
    for special_letter, normal_letter in letters_dictionary.items():
        for column in columns_list:
            players_stats[column] = players_stats[column].apply(lambda value: value.replace(special_letter, normal_letter))

    club_dictionary = {"Cracovia": "CRA", "Gornik Zabrze": "GOR", "Jagiellonia Bialystok": "JAG",
                       "Legia Warszawa": "LEG", "Lechia Gdansk": "LGD", "Lech Poznan": "LPO", "Piast Gliwice": "PIA",
                       "Podbeskidzie Bielsko-Biala": "POD", "Pogon Szczecin": "POG", "Rakow Czestochowa": "RCZ",
                       "Slask Wroclaw": "SLA", "PGE FKS Stal Mielec": "STM", "Warta Poznan": "WAR",
                       "Wisla Krakow": "WIS", "Wisla Plock": "WPL", "Zaglebie Lubin": "ZAG"}

    # adding club abbreviation
    for club_name, club_abr in club_dictionary.items():
        players_stats["club_abr"] = players_stats.apply(
            lambda ps: club_abr if ps["club"] == club_name else ps["club_abr"], axis=1)

    # changin names of status column
    status_dictionary = {"Pozaklubem": "out of club", "Występniepewny": "uncertain",
                         "Zawieszony": "suspended", "Kontuzjowany": "injury"}

    for status_name_old, status_name_new in status_dictionary.items():
        players_stats["status"] = players_stats.apply(
            lambda ps: status_name_new if ps["status"] == status_name_old else ps["status"], axis=1)

    print(players_stats)
    # saving dataframe
    players_stats.to_csv(path + r'\data\raw\ekstraclass\02_players_stats_{date}.csv'.format(date=var.time_stamp),
                         index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


