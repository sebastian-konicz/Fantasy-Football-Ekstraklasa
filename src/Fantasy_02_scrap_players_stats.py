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

    # loading file with links
    # links_df = pd.read_csv(project_dir + r'\data\raw\Players_links.csv')
    links_df = pd.read_csv(project_dir + r'\data\raw\Players_links_short.csv', delimiter=';')

    # creating list with links
    link_list = links_df["Link"].tolist()

    dataframes = []
    # looping throgu links
    for link in link_list:
        # gettig the page with stats for player
        driver = webdriver.Chrome(PATH)
        driver.get(link)

        # getting the site html
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        driver.quit()

        # PLAYER INFO

        # TABLE DATA
        table_body = site.find('tbody')
        table_rows = table_body.find_all('tr')
        # empty lists
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
        for row in table_rows:
            col = row.find_all('td')
            if len(col) == 15:
                pattern_lettes = re.compile("([A-Za-z])\w+")
                pattern_numbers = re.compile("([0-9])+")

                # round = col[0]
                # opponent = col[1]
                # gametime = row.find('td', title='Czas gry')
                # goals = row.find('td', title='Bramki')
                # assists = row.find('td', title='Asysty')
                # own_goal = row.find('td', title='Bramki samobójcze')
                # penalty = row.find('td', title='Karny wykorzystany')
                # penalty_won = row.find('td', title='Karny wywalczony')
                # penalty_given = row.find('td', title='Karny spowodowany')
                # penalty_lost = row.find('td', title='Karny zmarnowany')
                # penalty_defend = row.find('td', title='Karny obroniony')
                # instat = row.find('td', title='InStat Index')
                # yellow = row.find('td', title='Zółta kartka')
                # red = row.find('td', title='Czerwona kartka')
                # points = row.find('td', title='Punkty')


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
                instat = re.search(pattern_numbers, instat).group()
                col_instat.append(instat)

                yellow = col[12].text
                yellow = re.search(pattern_numbers, yellow).group()
                col_yellow.append(yellow)

                red = col[13].text
                red = re.search(pattern_numbers, red).group()
                col_red.append(red)

                points = col[14].text
                points = re.search(pattern_numbers, points).group()
                col_points.append(points)

            else:
                pass

        # zipping lists
        data_tuples = list(zip(col_round, col_opponent, col_time, col_goals, col_assists, col_own_goal, col_penalty,
                               col_penalty_won, col_penalty_given, col_penalty_lost, col_penalty_defend, col_instat,
                               col_yellow, col_red, col_points))

        # creating dataframe
        player_stats = pd.DataFrame(data_tuples, columns=["Round", "Opponent", "Time", "Goals", "Assists", "Own_goal",
                                                         "Penalty", "Penalty_won", "Penalty_given", "Penalty_lost",
                                                         "Penalty_defended", "InStat", "Yellow_card", "Red_card",
                                                         "Points"])
        print(player_stats)

        # saving dataframe
        player_stats.to_csv(project_dir + r'\data\raw\Players_stats.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


