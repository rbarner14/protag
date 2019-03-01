import sys # for running search at command line; may not be needed
import requests # for get requests
import time # for sleeping


SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
SONG_URL = "https://genius.com/api/songs/"
ARTIST_URL = "https://genius.com/api/artists/"
ALBUM_URL = "https://genius.com/api/albums/"

# adds to song url list (created in app call), return 1st 32 pages of producer's 
# song discography, sorted by views on Genius (popularity)
def get_songs_url_list(producer_id):

    for i in range(32):
        song_url = SONGS_URL % (producer_id, i+1)
        songs_by_producer_urls.append(song_url)

    print(songs_by_producer_urls) 

# get producer id
# important function as it is used to get producer and song data
def get_producer_id(producer_name):

    url = SEARCH_URL + producer_name

    print(url)

    r = requests.get(url)
    j = r.json()

    if j['meta']['status'] == 200 and j['response']['sections'][0]['type'] == 'artist' and len(j['response']['sections'][0]['hits']) != 0:
        genius_performer_id = j['response']['sections'][0]['hits'][0]['result']['id']
    else:
        genius_performer_id = "id not found"
        print(f"no {producer_name} found")

    return genius_performer_id


# return a "^" separated string of producer's name, img url and bio (long text)
# returning empty strings if values at keys do not exist
def get_producer_data(producer_name):

    producer_data = []

    url = ARTIST_URL + str(get_producer_id(producer_name))

    r = requests.get(url)
    j = r.json()

    if j['meta']['status'] == 200 and j['response']['artist']:
        
        genius_producer_name = j['response']['artist']['name']
        if j['response']['artist']['image_url']:
            producer_image_url = j['response']['artist']['image_url']
        else: 
            producer_image_url = ""
        if j['response']['artist']['description_preview']:
            bio = j['response']['artist']['description_preview']
        else: 
            bio = ""

        producer_data.append(f"{genius_producer_name}^{producer_image_url}^{bio}")

    return producer_data


# returns a "^" separated string of song details: 
# id, name, producer id, release date, and apple media player link
# sleep added to slow crawl/api requests
def get_song_data(producer_id):

    songs = [] # list to parse for csv/txt output
    song_urls = [] # list of song urls to gather data from

    for url in songs_by_producer_urls:
        print(url)

        r = requests.get(url)
        j = r.json()

        for song in j['response']['songs']: 
            song_id = song['id']
            song_url = SONG_URL + str(song_id)
            song_urls.append(song_url)

        time.sleep(1)

    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:
        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        if j2['response']['song']['id'] != None: 
            song_id = j2['response']['song']['id']
        else: 
            song_id = ""

        if j2['response']['song']['title'] != None:
            song_title = j2['response']['song']['title']
        else: 
            song_title = ""

        if j2['response']['song']['release_date'] != None:
            release_date = j2['response']['song']['release_date']
        else:
            release_date = ""

        if j2['response']['song']['apple_music_player_url'] != None:
            apple_music_player_url = j2['response']['song']['apple_music_player_url']
        else: 
            apple_music_player_url = ""

        if j2['response']['song']['release_date_components'] != None:
            if j2['response']['song']['release_date_components']['year']:
                release_year = j2['response']['song']['release_date_components']['year']
            else: 
                release_year = ""

            if j2['response']['song']['release_date_components']['month'] != None:
                release_month = j2['response']['song']['release_date_components']['month']
            else: 
                release_month = ""

            if j2['response']['song']['release_date_components']['day'] != None:
                release_day =j2['response']['song']['release_date_components']['day']
            else: 
                release_day = ""
        else: 
            release_year = ""
            release_month = ""
            release_day = ""
            perfomer_id = ""

        if j2['response']['song']['primary_artist']['id'] != None:
            performer_id = j2['response']['song']['primary_artist']['id']
        else: 
            perfomer_id = ""

        if j2['response']['song']['album'] != None: 
            album_id = j2['response']['song']['album']['id']
        else: 
            album_id = ""
            
        songs.append(f"{song_id}^{song_title}^{album_id}^{performer_id}^{release_date}^{release_year}^{release_month}^{release_day}^{apple_music_player_url}")

        time.sleep(1)

    return songs



################################################################################

if __name__ == '__main__':
    # list of producers to read for crawling; could also import
    producer_list = open("producer_list_pt_3.txt")

    # create and write to csvs & text files; csvs for better view of txt python will use
    # producer data
    with open('producer_data_scrape_txt_3.txt', 'w') as f:
        f.write("producer_id, producer_name, producer_img_url, bio\n")

    with open('producer_data_scrape_csv_3.csv', 'w') as f:
        f.write("producer_id, producer_name, producer_img_url, bio\n")

    #song data
    with open('song_data_scrape_txt_3.txt', 'w') as f:
        f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")

    with open('song_data_scrape_csv_3.csv', 'w') as f:
        f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")


    for producer in producer_list:
        # producer name populated from provided list
        producer_name = producer

        # do not start data gathering process unless artist search returns hits
        # otherwise gather and populate csv and txt files with 
        # producer and song data
        if get_producer_id(producer_name) != "id not found":
            producer_id = get_producer_id(producer_name)
            producer_data = get_producer_data(producer_name)
            songs_by_producer_urls = []

            get_songs_url_list(producer_id)

            songs = get_song_data(producer_id)

            # pipe delimited text file which will be parsed by separate script
            with open('producer_data_scrape_txt_3.txt', 'a') as f:
                for data in producer_data:
                    producer_data_components = data.split("^")
                    f.write(
                        str(producer_id) + "|" + str(producer_data_components[0]) + 
                        "|" + str(producer_data_components[1]) + "|" + 
                        str(producer_data_components[2]) +
                        "\n"
                    )

            # csv for better view and problem diagnosis than 
            # that achieved through txt file
            with open('producer_data_scrape_csv_3.csv', 'a') as f:
                for data in producer_data:
                    f.write(
                        str(producer_id) + "," + str(producer_data_components[0]) + 
                        "," + str(producer_data_components[1]) + "," + 
                        str(producer_data_components[2]) +
                        "\n"
                    )


            with open('song_data_scrape_txt_3.txt', 'a') as f:
                for song in songs:
                    split_songs = song.split("^")
                    f.write(
                        str(split_songs[0]) + "|" + str(split_songs[1]) + "|" + 
                        str(split_songs[2]) + "|" + str(split_songs[3]) + "|" +
                        str(split_songs[4]) + "|" + str(split_songs[5]) + "|" +
                        str(split_songs[6]) + "|" + str(split_songs[7]) + "|" +
                        str(split_songs[8]) + 
                        "\n"
                    )


            with open('song_data_scrape_csv_3.csv', 'a') as f:
                for song in songs:
                    split_songs = song.split("^")
                    f.write(
                        str(split_songs[0]) + "," + str(split_songs[1]) + "," + 
                        str(split_songs[2]) + "," + str(split_songs[3]) + "," +
                        str(split_songs[4]) + "," + str(split_songs[5]) + "," +
                        str(split_songs[6]) + "," + str(split_songs[7]) + "," +
                        str(split_songs[8]) +
                        "\n"
                    )

            # print song to console for progress tracking
            for s in songs:
                print(s) 
