from pathlib import Path
import datetime as dt

# chrome driver path
chrome_driver = r'C:\Users\kose9001\Desktop\JTM\chromedriver.exe'

# project directory
project_dir = str(Path(__file__).resolve().parents[2])

# ekstraklasa site with players links
first_league_players = 'https://fantasy.1liga.org/pl/stats'

# ekstraklasa site with current match scores
ekstraclass_current_match_scores = 'https://ekstraklasa.org/rozgrywki/terminarz/ekstraklasa-4'

# time stamp
today = dt.date.today()
day = today.strftime("%d")
month = today.strftime("%b").upper()
year = today.strftime("%y")
time_stamp = day + month + year