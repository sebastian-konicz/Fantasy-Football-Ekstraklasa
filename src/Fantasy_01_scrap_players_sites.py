from bs4 import BeautifulSoup
from pathlib import Path
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

    # gettig the main page with fantasy soccer stat
    driver = webdriver.Chrome(PATH)
    driver.get('https://fantasy.ekstraklasa.org/stats')

    site_list =[]
    # looping throug pagination (only 28 sites - gave 30 to be sure)
    for i in range(30):
        # getting the site
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        # adding site to site_list
        site_list.append(site)
        # getting the button for the next site
        next_button = driver.find_element_by_link_text('Następny')
        # going to the next site
        next_button.click()

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
            link = 'https://fantasy.ekstraklasa.org' + a['href']
            # appending lists
            players_list.append(player)
            links_list.append(link)

    # zipping lists
    data_tuples = list(zip(players_list, links_list))

    # creating dataframe
    players_links_df = pd.DataFrame(data_tuples, columns=['Player', 'Link'])

    # saving dataframe
    players_links_df.to_csv(project_dir + r'\data\raw\Players_links.csv', index=False, encoding='UTF-8')

    # shutting down selenium driver
    driver.quit()

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


