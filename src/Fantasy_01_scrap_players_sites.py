from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd
import time
from selenium import webdriver

PATH = r'C:\Users\kose9001\Desktop\JTM\chromedriver.exe'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # Getti
    main_page = requests.get('https://fantasy.ekstraklasa.org/stats')
    html_main_page = BeautifulSoup(main_page.content, 'html.parser')
    links_years = html_main_page.find_all("tbody")

    driver = webdriver.Chrome(PATH)
    driver.get('https://fantasy.ekstraklasa.org/stats')

    site_list =[]
    for i in range(30):
        next_button = driver.find_element_by_link_text('Następny')
        site_list.append(next_button)
        print(next_button)
        next_button.click()

    print(site_list)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table_body = soup.find_all('td', class_="sorting_1")
    # table_links = table_body.find_all("a")
    # player_link = table_body.get('href')

    for td in table_body:
        a = td.find_all("a")
        print(a)


    print(table_body)
    # print(player_link)


    driver.quit()

if __name__ == "__main__":
    main()


