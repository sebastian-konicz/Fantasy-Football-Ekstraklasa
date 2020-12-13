import src.first_league.first_league_00_variables as var
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    # gettig the main page with fantasy soccer stat
    driver = webdriver.Chrome(var.chrome_driver)
    driver.get(var.first_league_players)

    site_list =[]
    # looping throug pagination (only 28 sites)
    for i in range(29):
        # getting around cookie acceptance button
        if i == 0:
            cookie_button = driver.find_element_by_partial_link_text("OK,")
            cookie_button.click()
        else:
            pass
        # getting the site
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        # adding site to site_list
        site_list.append(site)
        # getting the button for the next site
        next_button = driver.find_element_by_link_text('Następny')
        # going to the next site
        if i < 28:
            next_button.click()
        else:
            pass

    # empty lists for values
    players_list = []
    links_list = []

    # looping thgrou sites
    for site in site_list:
        # getting rows form table
        table_body = site.find_all('td', class_="sorting_1")
        for td in table_body:
            # getting a tag with player's name and link
            a = td.find("a")
            # player name
            player = a.text
            # link to player's stats
            link = 'https://fantasy.1liga.org/pl' + a['href']
            # appending lists
            players_list.append(player)
            links_list.append(link)

    # zipping lists
    data_tuples = list(zip(players_list, links_list))

    # creating dataframe
    players_links_df = pd.DataFrame(data_tuples, columns=['player', 'link'])

    # saving dataframe
    players_links_df.to_csv(path + r'\data\raw\first_league\01_players_links_{date}.csv'.format(date=var.time_stamp),
                            index=False, encoding='UTF-8')

    # shutting down selenium driver
    driver.quit()

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


