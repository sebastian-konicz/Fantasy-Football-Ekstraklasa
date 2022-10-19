import src.ekstraclass.ekstraclass_00_variables as var
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # variables
    season = '2021_2022'
    round = 'test'

    # output files
    # players_links_path = r'\data\raw\ekstraclass\01_players_links_{date}.csv'.format(date=var.time_stamp)
    gminy_names_path = r'\data\bps\raw\gminy_names_short.csv'
    # gminy_names_path = r'\data\bps\raw\gminy_names.csv'
    gminy_file_path = r'\data\bps\final\gminy_names_final.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    # gminy dataframe
    gm = pd.read_csv(path + gminy_names_path)

    # reshaping and cleaning df
    gm['gmi_name'] = gm['gmi_name'].apply(lambda x: str(x).lower().replace('gmina ', ''))
    print(gm.head())

    # saving dataframe
    gm.to_csv(path + gminy_file_path, index=False)

    # dataframe to lis
    gm_list = gm['gmi_name'].to_list()

    print(gm_list)

    # bps site
    bps_www = 'https://mojbank.pl/znajdz-placowke'

    for gmina in gm_list:
        print(gmina)
        # gettig the main page with fantasy soccer stat
        driver = webdriver.Chrome(var.chrome_driver)
        driver.get(bps_www)

        # getting the button for the next site
        inputElement = driver.find_element_by_name('cruzmap-location')
        driver.implicitly_wait(100)
        inputElement.send_keys(gmina)
        driver.implicitly_wait(100)
        inputElement.send_keys(Keys.ENTER)
        driver.implicitly_wait(100)
        inputElement.send_keys(Keys.ARROW_UP)
        time.sleep(0.5)

        # prnit('dupa')

        # driver.execute_script("""
        # var input = document.getElementById("cruzmap-location");
        # input.addEventListener("keyup", function(event)
        # {if (event.keyCode === 13)
        #     {event.preventDefault();
        #     document.getElementById("cruzmap-search").click();
        # }
        # });
        # """)

        # cruz_map_location = driver.find_element("id", "cruzmap-location")
        # driver.implicitly_wait(100)
        # cruz_map_location.send_keys(Keys.ARROW_UP)
        # print(cruz_map_location)
        #
        # # getting the button for the next site
        # next_button = driver.find_element("id", 'cruzmap-search')
        # print(next_button)
        # # going to the next site
        # next_button.click()

        # getting the site
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')

        # print(site)

        # print(site)
        all_divs = driver.find_element("id", 'cruzmap-points')
        print(all_divs)
        div_html = all_divs.get_attribute('innerHTML')
        print(div_html)

        # all_divs_2 = site.find_all('div', id="cruzmap-points")
        # print(all_divs_2)

        point_info = BeautifulSoup(div_html, 'html.parser')

        all_points = point_info.find_all('div', class_="point-info")
        print(all_points)



        #
        # points_length = len(all_divs)
        #
        # if points_length == 0:
        #     print('brak punktow w okolicy')
        #     pass
        # else:
        #     print(all_divs)

        # shutting down selenium driver
        driver.quit()

    # map_html = cruz_map.get_attribute('innerHTML')
    #
    # print(map_html)

    # point = driver.find_element_by_class_name('point_info')
    # points = driver.find_elements_by_class_name('point_info')
    #
    # print(point)
    # print(points)

    # html = driver.page_source
    # site = BeautifulSoup(html, 'html.parser')
    # print(site)
    # all_divs = site.find_all('div', class_="point_info")
    # print(all_divs)

    #
    # # empty lists for values
    # players_list = []
    # links_list = []
    #
    # # looping thgrou sites
    # for site in site_list:
    #     # getting rows form table
    #     table_body = site.find_all('td', class_="sorting_1")
    #     for td in table_body:
    #         # getting a tag with player's name and link
    #         a = td.find("a")
    #         # player name
    #         player = a.text
    #         # link to player's stats
    #         link = 'https://fantasy.ekstraklasa.org' + a['href']
    #         # appending lists
    #         players_list.append(player)
    #         links_list.append(link)
    #
    # # zipping lists
    # data_tuples = list(zip(players_list, links_list))
    #
    # # creating dataframe
    # players_links_df = pd.DataFrame(data_tuples, columns=['player', 'link'])
    #
    # # saving dataframe
    # players_links_df.to_csv(path + players_links_path, index=False, encoding='UTF-8')



    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


