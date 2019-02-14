import sys # for running search at command line; may not be needed
import time # for sleeping

import requests # for get requests


SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
SONG_URL = "https://genius.com/api/songs/"
ARTIST_URL = "https://genius.com/api/artists/"
ALBUM_URL = "https://genius.com/api/albums/"
NUM_SONGS = 2
NUM_SONG_PAGES = 2

# adds to song url list (created in app call), return 1st 32 pages of producer's 
# song discography, sorted by views on Genius (popularity)
def get_songs_url_list(producer_id):

    urls = []

    for i in range(NUM_SONG_PAGES):
        song_url = SONGS_URL % (producer_id, i+1)
        urls.append(song_url)

    print(urls)
    return urls

# get producer id
# important function as it is used to get producer and song data
def get_producer_id(producer_name):

    url = SEARCH_URL + producer_name

    print(url)

    r = requests.get(url)
    j = r.json()
    page_response = j['meta']['status']
    first_search_section = j['response']['sections'][0]
    search_hits = first_search_section['hits']

    if page_response == 200 and first_search_section['type'] == 'artist' and len(search_hits) != 0:
        genius_performer_id = search_hits[0]['result']['id']
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
    page_response = j['meta']['status']
    artist_obj = j['response']['artist']

    if page_response == 200 and artist_obj:
        
        genius_producer_name = artist_obj['name']
        producer_image_url = artist_obj.get('image_url',"")
        bio = artist_obj.get('description_preview',"")

        producer_data.append(f"{genius_producer_name}^{producer_image_url}^{bio}")

    return producer_data


# returns a "^" separated string of song details: 
# id, name, producer id, release date, and apple media player link
# sleep added to slow crawl/api requests
def get_song_data(producer_id, songs_by_producer_urls):

    songs = [] # list to parse for csv/txt output
    song_urls = [] # list of song urls to gather data from

    for url in songs_by_producer_urls:
        print(url)

        r = requests.get(url)
        j = r.json()

        song_count = 0
        for song in j['response']['songs']: 
            if song_count < NUM_SONGS:
                song_count += 1
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

        song_json = j2['response']['song']

        release_date_components = song_json['release_date_components']
        performer = song_json['primary_artist']
        album = song_json['album']
        song_id = song_json.get('id', "")
        song_title = song_json.get('title', "")
        apple_music_player_url = song_json.get('apple_music_player_url', "")
        release_date = song_json.get('release_date', "")
        
        if release_date_components:
            release_year = release_date_components.get('year', "")
            release_month = release_date_components.get('month', "")
            release_day = release_date_components.get('day', "")
        else: 
            release_year = ""
            release_month = ""
            release_day = ""

        performer_id = performer.get('id', "")

        if album:
            album_id = album.get('id', "")
        else:
            album_id = ""
            
        songs.append(f"{song_id}^{song_title}^{album_id}^{performer_id}^{release_date}^{release_year}^{release_month}^{release_day}^{apple_music_player_url}")

        time.sleep(1)

    return songs

def write_headers(filename, headers, delimiter):
        # w = write to new file
    with open(filename, 'w') as f:
        f.write(delimiter.join(headers))

def populate_producer_data(filenames):
    i = 1
    if i > len(filenames):
        # a = append to already created file
        with open(filenames[i], 'a') as f:
            for data in producer_data:
                producer_rows = data.split("^")
                f.write(str(producer_id) + delimiters[i] + delimiters[i].join(producer_rows) + "\n")
        i += 1

def populate_song_data(filenames):
    i = 1
    if i > len(filenames):
        with open(filenames[i], 'a') as f:
            for song in songs:
                song_rows = songs.split("^")
                f.write(delimiters[i].join(song_rows) + "\n")
        i += 1


################################################################################

if __name__ == '__main__':
    # list of producers to read for crawling; could also import
    producer_list = open("producer_list_test.txt")

    producer_columns = ["producer_id", "producer_name", "producer_img_url",
                        "bio"]
    song_columns = ["song_id", "song_title", "album_id", "performer_id", 
                    "release_date", "release_year", "release_month", 
                    "release_day", "apple_music_player_url"]
    producer_filenames = ["producer_data.txt", "producer_data.csv"]
    song_filenames = ["song_data.txt", "song_data.csv"]
    delimiters = ["|", ","] 

    write_headers("producer_data.txt", producer_columns, "|")
    write_headers("producer_data.csv", producer_columns, ",")
    write_headers("song_data.txt", song_columns, "|")
    write_headers("song_data.csv", song_columns, ",")

    # create and write to csvs & text files; csvs for better view of txt python will use
    # producer data

    # write_headers("producer_data_scrape_rd.txt", )
    # with open('producer_data_scrape_rd.txt', 'w') as f:
    #     f.write("producer_id, producer_name, producer_img_url, bio\n")

    # with open('producer_data_scrape_rd.csv', 'w') as f:
    #     f.write("producer_id, producer_name, producer_img_url, bio\n")

    # #song data
    # with open('song_data_scrape_rd.txt', 'w') as f:
    #     f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")

    # with open('song_data_scrape_rd.csv', 'w') as f:
    #     f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")


    for producer in producer_list:
        # producer name populated from provided list
        producer_name = producer

        # do not start data gathering process unless artist search returns hits
        # otherwise gather and populate csv and txt files with 
        # producer and song data
        if get_producer_id(producer_name) != "id not found":
            producer_id = get_producer_id(producer_name)
            producer_data = get_producer_data(producer_name)
            songs_by_producer_urls = get_songs_url_list(producer_id)

            songs = get_song_data(producer_id, songs_by_producer_urls)


            populate_producer_data(producer_filenames)
            populate_song_data(song_filenames)


            # pipe delimited text file which will be parsed by separate script
            # with open('producer_data_scrape_txt_3.txt', 'a') as f:
            #     for data in producer_data:
            #         producer_data_components = data.split("^")
            #         f.write(
            #             str(producer_id) + "|" + str(producer_data_components[0]) + 
            #             "|" + str(producer_data_components[1]) + "|" + 
            #             str(producer_data_components[2]) +
            #             "\n"
            #         )

            # csv for better view and problem diagnosis than 
            # that achieved through txt file

            # with open('producer_data_scrape_csv_3.csv', 'a') as f:
            #     for data in producer_data:
            #         f.write(
            #             str(producer_id) + "," + str(producer_data_components[0]) + 
            #             "," + str(producer_data_components[1]) + "," + 
            #             str(producer_data_components[2]) +
            #             "\n"
            #         )


            # with open('song_data_scrape_txt_3.txt', 'a') as f:
            #     for song in songs:
            #         song_parts = song.split("^")
            #         f.write("|".join(song_parts) + "\n")

            # with open('song_data_scrape_csv_3.csv', 'a') as f:
            #     for song in songs:
            #         split_songs = song.split("^")
            #         f.write(
            #             str(split_songs[0]) + "," + str(split_songs[1]) + "," + 
            #             str(split_songs[2]) + "," + str(split_songs[3]) + "," +
            #             str(split_songs[4]) + "," + str(split_songs[5]) + "," +
            #             str(split_songs[6]) + "," + str(split_songs[7]) + "," +
            #             str(split_songs[8]) +
            #             "\n"
            #         )

            # print song to console for progress tracking
            for s in songs:
                print(s) 
