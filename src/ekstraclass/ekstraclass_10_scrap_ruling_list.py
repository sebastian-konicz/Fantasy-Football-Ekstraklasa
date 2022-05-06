import src.ekstraclass.ekstraclass_00_variables as var
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # variables

    # output files
    # players_links_path = r'\data\raw\ekstraclass\01_players_links_{date}.csv'.format(date=var.time_stamp)
    players_links_path = r'\data\raw\rulings.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    # gettig the main page with fantasy soccer stat
    driver = webdriver.Chrome(var.chrome_driver)
    driver.get('https://orzeczenia.nsa.gov.pl/cbo/find?p=1&q=+SZUKANE+%5B%22gmina+podatnik+VAT%22%5D+ZORZ+%5Btrue%5D')

    site_list =[]

    # looping throug pagination (only 33 sites)
    for i in range(0, 1):
        # getting the site
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        # adding site to site_list
        site_list.append(site)
        # getting the button for the next site
        next_button = driver.find_element_by_link_text('następna »')
        # going to the next site
        next_button.click()

    # empty lists for values
    signature_list = []
    links_list = []

    # looping thgrou sites
    for site in site_list:
        # getting rows form table
        table_body = site.find_all('table', class_="info-list pb-none")
        for td in table_body:
            # print(td)
            # getting a tag with player's name and link
            a = td.find("a")
            # player name
            signature = a.text.strip()
            print(signature)
            # link to player's stats
            print(a['href'])
            link = 'https://orzeczenia.nsa.gov.pl/' + a['href']
            # appending lists
            signature_list.append(signature)
            links_list.append(link)

    # zipping lists
    data_tuples = list(zip(signature_list, links_list))

    # creating dataframe
    players_links_df = pd.DataFrame(data_tuples, columns=['ruling', 'link'])

    # saving dataframe
    players_links_df.to_csv(path + players_links_path, index=False) #encoding='UTF-8'

    # shutting down selenium driver
    driver.quit()

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


