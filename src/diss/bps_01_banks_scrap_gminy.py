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
    # gminy_names_path = r'\data\bps\raw\gminy_names_short.csv'
    gminy_names_path = r'\data\bps\raw\gminy_names.csv'
    gminy_file_path = r'\data\bps\final\gminy_names_final.csv'
    final_file_path = r'\data\bps\final\point_adress_all.csv'

    # start time of function
    start_time = time.time()

    # project directory
    path = var.project_dir

    # gminy dataframe
    gm = pd.read_csv(path + gminy_names_path, sep=',')

    # reshaping and cleaning df
    gm['pow_teryt'] = gm['pow_teryt'].apply(lambda x: str(x).zfill(4))
    gm['gmi_name'] = gm['gmi_name'].apply(lambda x: str(x).lower().replace('gmina ', ''))
    gm['pow_name'] = gm['pow_name'].apply(lambda x: str(x).lower().replace('powiat ', ''))

    print(gm.head())

    # saving dataframe
    gm.to_csv(path + gminy_file_path, index=False)

    # dataframe to lis
    gm_list = gm['gmi_name'].to_list()
    teryt_list = gm['pow_teryt'].to_list()

    gm_dict = dict(zip(gm_list, teryt_list))

    # bps site
    bps_www = 'https://mojbank.pl/znajdz-placowke'

    df_list = []

    for gmina, teryt in gm_dict.items():
        print(gmina, teryt)

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
        # time.sleep(0.5)
        time.sleep(2.5)

        # getting div with points data
        all_divs = driver.find_element("id", 'cruzmap-points')
        div_html = all_divs.get_attribute('innerHTML')
        # print(div_html)

        # parsing div_html
        point_info = BeautifulSoup(div_html, 'html.parser')
        all_points = point_info.find_all('div', class_="point-info")

        points_length = len(all_points)

        # empty listst
        point_id_list = []
        point_name_list = []
        point_street_list = []
        point_address_list = []
        point_teryt_list = []
        point_gmina_list = []
        point_phone_list = []
        point_url_list = []

        if points_length == 0:
            print('brak punktow w okolicy')
            pass
        else:
            for point in all_points:
                point_id = point.get('id')
                # point_teryt = teryt
                point_name = point.find('div', class_='point-name').text
                point_street = point.find('div', class_='point-street').text
                point_address = point.find('div', class_='point-address').text
                point_teryt = teryt
                point_gmina = gmina
                try:
                    point_phone = point.find('div', class_='point-phone').text
                except AttributeError:
                    point_phone = ''
                    print("There's no telephone value")
                try:
                    point_url = point.find('div', class_='point-url').text
                except AttributeError:
                    point_url = ''
                    print("There's no url value")

                print(point_name)

                point_id_list.append(point_id)
                point_name_list.append(point_name)
                point_street_list.append(point_street)
                point_address_list.append(point_address)
                point_teryt_list.append(point_teryt)
                point_gmina_list.append(point_gmina)
                point_phone_list.append(point_phone)
                point_url_list.append(point_url)

        data_tuples = list(zip(point_id_list, point_name_list,
                               point_street_list, point_address_list,
                               point_teryt_list, point_gmina_list,
                               point_phone_list, point_url_list))

        point_data = pd.DataFrame(data_tuples, columns=["id", "name",
                                                        "street", "adress",
                                                        "pow_teryt", "gmina_town",
                                                        "phone", "url"])

        df_list.append(point_data)
        # saving dataframe
        points_interim_pat = r'\data\bps\interim\points_{gmina}.csv'.format(gmina=gmina)
        point_data.to_csv(path + points_interim_pat, index=False)

        # shutting down selenium driver
        driver.quit()

    df_final = pd.concat(df_list)

    df_final.drop_duplicates(subset=['id'], keep='first', inplace=True)
    df_final.reset_index(inplace=True)

    df_final = df_final.merge(gm,
                              how='left',
                              left_on=["pow_teryt", "gmina_town"],
                              right_on=["pow_teryt", "gmi_name"])

    df_final = df_final[["id", "name", "street", "adress",
                        "pow_teryt", "pow_name", "gmina_town",
                        "phone", "url"]]

    print(df_final.head())
    print("długosc całego dataframu")
    print(len(df_final.index))

    # saving dataframe
    df_final.to_csv(path + final_file_path, index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()


