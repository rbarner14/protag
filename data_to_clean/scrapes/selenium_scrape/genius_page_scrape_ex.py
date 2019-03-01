# from selenium import webdriver

# #done in Chrome
# chromedriver = "/home/vagrant/src/project/protag/chromedriver"
# # driver = webdriver.Chrome(chromedriver)
# # driver.get("https://genius.com/artists/The-neptunes")

# # Open up a Firefox browser and navigate to web page
# # browser= webdriver.Firefox(executable_path='/home/vagrant/src/project/protag')
# # driver.get("https://genius.com/artists/The-neptunes")

# # Extract lists of "songs" and "artists" based on xpath
# # can find by css, other tags, etc; look up find_elements_by methods
# # // proceed most xpaths
# # want it to be in a div tag
# # in div tag, title should correspond to song-name
# # songs = songs.find_elements_by_xpath('//div[@title="song-name"]')

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# creates .csv file and column headers
with open('result2.csv', 'w') as f:
    f.write("Songs, Artists, Producer \n")

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(executable_path='/Users/ryanbarner⁩/src⁩/project⁩/protag⁩/scrapes/selenium_scrape/chromedriver')

# go to the google home page
driver.get("https://genius.com/artists/The-neptunes")

# the page is ajaxy so the title is originally this:
# print(driver.title)

songs = driver.find_elements_by_xpath('//div[@class="mini_card-title"]')
artists = driver.find_elements_by_xpath('//div[@class="mini_card-subtitle"]')
num_song_items = len(songs)

# populates csv file
with open('result2.csv', 'a') as f:
    for i in range(num_song_items):
        f.write(songs[i].text + " , " + artists[i].text + "\n")

driver.close()
# find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")

# # type in the search
# inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
# inputElement.submit()

# try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    # WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # You should see "cheese! - Google Search"
    # print(driver.title)

# finally:
driver.quit()