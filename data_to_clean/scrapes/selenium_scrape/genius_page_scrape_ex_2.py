# Extract lists of "songs" and "artists" based on xpath
# can find by css, other tags, etc; look up find_elements_by methods
# // proceed most xpaths
# want it to be in a div tag
# in div tag, title should correspond to song-name
# songs = songs.find_elements_by_xpath('//div[@title="song-name"]')

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# creates .csv file and column headers
with open('result3.csv', 'w') as f:
    f.write("Songs, Artists, Producer \n")

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path='/Users/ryanbarner⁩/src⁩/project⁩/protag⁩/scrapes/selenium_scrape/chromedriver')

# go to the URL
driver.get("/Users/ryanbarner⁩/src⁩/project⁩/api_scrape/geniu_api_scrape/lex_luger_genius_artist_page.html")

songs = driver.find_elements_by_xpath('//div[@class="mini_card-title"]')
artists = driver.find_elements_by_xpath('//div[@class="mini_card-subtitle"]')
num_song_items = len(songs)

# populates csv file
with open('result3.csv', 'a') as f:
    for i in range(num_song_items):
        f.write(songs[i].text + " , " + artists[i].text + "\n")

driver.close()
driver.quit()