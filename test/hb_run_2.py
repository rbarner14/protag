import sys # for running search at command line; may not be needed
import time # for sleeping

import requests # for get requests


SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
SONG_URL = "https://genius.com/api/songs/"
ARTIST_URL = "https://genius.com/api/artists/"
ALBUM_URL = "https://genius.com/api/albums/"
NUM_SONG_PAGES = 40

# adds to song url list (created in app call), return 1st 32 pages of producer's 
# song discography, sorted by views on Genius (popularity)
def get_songs_url_list(producer_id):

    urls = []

    for i in range(NUM_SONG_PAGES):
        song_url = SONGS_URL % (producer_id, i+1)
        urls.append(song_url)

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
        producer_id = search_hits[0]['result']['id']
    else:
        producer_id = "id not found"
        print(f"no {producer_name} found")

    return producer_id


# return a "^" separated string of producer's name, img url and bio (long text)
# returning empty strings if values at keys do not exist
def get_producer_data(producer_id):

    producer_data = []

    url = ARTIST_URL + str(producer_id)

    r = requests.get(url)
    j = r.json()
    page_response = j['meta']['status']
    artist_obj = j['response']['artist']

    if page_response == 200 and artist_obj:
        
        genius_producer_name = artist_obj['name']
        producer_image_url = artist_obj.get('image_url',"")

        producer_data.append(f"{genius_producer_name}^{producer_image_url}")

    return producer_data


def generate_data(songs_by_producer_urls):
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

    return song_urls


# returns a "^" separated string of song details: 
# id, name, producer id, release date, and apple media player link
# sleep added to slow crawl/api requests
def get_produce_song_data(producer_id, songs_by_producer_urls):

    songs = [] # list to parse for csv/txt output
    song_urls = generate_data(songs_by_producer_urls)

    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:

        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        song_request = j2.get('response',"")

        if song_request not in (None, ""):
            song_json = song_request['song']

                # value at key could be none, these conditional spaces replace them with
                # an empty string
            performer = song_json['primary_artist']
            performer_id = performer.get('id', "")
            performer_name = performer.get('name', "")

            if performer['image_url'] != None:
                performer_img_url = performer.get('image_url', "")
            else:
                performer_img_url = ""

            song_id = song_json.get('id', "")
            song_title = song_json.get('title', "")
            apple_music_player_url = song_json.get('apple_music_player_url', "")
            
            album = song_json.get('album',"")

            if album not in (None, ""):
                album_id = album.get('id', "")
                album_title = album.get('name', "")
                cover_art_url = album.get('cover_art_url', "")
            else:
                album_id = ""
                album_title = ""
                cover_art_url = ""

            if song_json['release_date'] != None:
                song_release_date = song_json.get('release_date', "")
            else: 
                song_release_date = ""

            if song_json['release_date_components'] != None:
                song_release_date_components = song_json.get('release_date_components', "")
            else: 
                song_release_date_components = ""
            
            if song_release_date_components != "":
                song_release_year = song_release_date_components.get('year', "")
                song_release_month = song_release_date_components.get('month', "")
                song_release_day = song_release_date_components.get('day', "")
            else: 
                song_release_year = ""
                song_release_month = ""
                song_release_day = ""

            performer_id = performer.get('id', "")
                
            songs.append(f"{song_id}^{song_title}^{album_id}^{album_title}^{cover_art_url}^{performer_id}^{performer_name}^{performer_img_url}^{song_release_date}^{song_release_year}^{song_release_month}^{song_release_day}^{apple_music_player_url}^{producer_id}")

            time.sleep(1)

    return songs

def get_events_data(producer_id, songs_by_producer_urls):

    events = [] # list to parse for csv/txt output
    song_urls = generate_data(songs_by_producer_urls)

    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:

        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        song_request = j2.get('response',"")

        if song_request not in (None, ""):
            song_json = song_request['song']

            # value at key could be none, these conditional spaces replace them with
            # an empty string
            performer = song_json['primary_artist']
            performer_id = performer.get('id', "")

            song_id = song_json.get('id', "")
            
            album = song_json.get('album',"")

            if album not in (None, ""):
                album_id = album.get('id', "")
                album_title = album.get('name', "")
                cover_art_url = album.get('cover_art_url', "")
            else:
                album_id = ""
                album_title = ""
                cover_art_url = ""

            performer_id = performer.get('id', "")
                
            events.append(f"{producer_id}^{performer_id}^{song_id}^{album_id}")

            time.sleep(1)

    return events

def get_song_data(songs_by_producer_urls):

    songs = [] # list to parse for csv/txt output
    song_urls = generate_data(songs_by_producer_urls) # list of song urls to gather data from

    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:

        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        song_request = j2.get('response',"")

        if song_request not in (None, ""):
            song_json = song_request['song']

            # value at key could be none, these conditional spaces replace them with
            # an empty string
            song_id = song_json.get('id', "")
            song_title = song_json.get('title', "")
            apple_music_player_url = song_json.get('apple_music_player_url', "")

            song_release_date = song_json.get('release_date', "")
            

            if song_release_date == None:
                song_release_date = ""

            if song_release_date not in (None, ""):
                song_release_date_components = song_json.get('release_date_components', "")
            else: 
                song_release_date_components = ""
            
            if song_release_date_components not in (None, ""):
                song_release_year = song_release_date_components.get('year', "")
                song_release_month = song_release_date_components.get('month', "")
                song_release_day = song_release_date_components.get('day', "")
            else: 
                song_release_year = ""
                song_release_month = ""
                song_release_day = ""
                
            songs.append(f"{song_id}^{song_title}^{song_release_date}^{song_release_year}^{song_release_month}^{song_release_day}^{apple_music_player_url}")

            time.sleep(1)

    return songs


def get_performer_data(songs_by_producer_urls):

    performers = [] # list to parse for csv/txt output
    song_urls = generate_data(songs_by_producer_urls)

    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:

        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        song_request = j2.get('response',"")

        if song_request not in (None, ""):
            song_json = song_request['song']

            # value at key could be none, these conditional spaces replace them with
            # an empty string
            performer = song_json['primary_artist']
            performer_id = performer.get('id', "")
            performer_name = performer.get('name', "")

            if performer['image_url'] != None:
                performer_img_url = performer.get('image_url', "")
            else:
                performer_img_url = ""

            performer_id = performer.get('id', "")
                
            performers.append(f"{performer_id}^{performer_name}^{performer_img_url}")

            time.sleep(1)

    return performers


def get_album_data(songs_by_producer_urls):

    albums = [] # list to parse for csv/txt output
    
    song_urls = generate_data(songs_by_producer_urls)
    # loop through song url list created, returning nulls for keys 
    # that do not exist
    for url in song_urls:

        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        song_request = j2.get('response',"")

        if song_request not in (None, ""):
            song_json = song_request['song']

        # value at key could be none, these conditional spaces replace them with
        # an empty string
        
            album = song_json.get('album',"")

            if album not in (None, ""):
                album_id = album.get('id', "")
                album_title = album.get('name', "")
                cover_art_url = album.get('cover_art_url', "")
                album_release_date_components = song_json['album']['release_date_components']
            else:
                album_id = ""
                album_title = ""
                cover_art_url = ""
                album_release_date_components = None

            if album_release_date_components not in (None, ""):
                album_release_year = album_release_date_components.get("year", "")
                album_release_month = album_release_date_components.get("month", "")
                album_release_day = album_release_date_components.get("day", "")
            else:
                album_release_year = ""
                album_release_month = ""
                album_release_day = ""
                
            albums.append(f"{album_id}^{album_title}^{cover_art_url}^{album_release_year}^{album_release_month}^{album_release_day}")

            time.sleep(1)

    return albums


# create files and write headers to them
def write_headers(filename, headers, delimiter):
        # w = write to new file
    with open(filename, 'w') as f:
        f.write(delimiter.join(headers)+ "\n")

# append ('a') data to producer file already created
def populate_producer_data(filename, delimiter):
    with open(filename, 'a') as f:
        for data in producer_data:
            producer_rows = data.split("^")
            f.write(str(producer_id) + delimiter + delimiter.join(producer_rows) + "\n")

def populate_events_data(filename, delimiter):
    with open(filename, 'a') as f:
        for event in events:
            event_rows = event.split("^")
            f.write(delimiter.join(event_rows) + "\n")

def populate_produce_song_data(filename, delimiter):
    with open(filename, 'a') as f:
        for song in produce_songs:
            song_rows = song.split("^")
            f.write(delimiter.join(song_rows) + "\n")

def populate_song_data(filename, delimiter):
    with open(filename, 'a') as f:
        for song in songs:
            song_rows = song.split("^")
            f.write(delimiter.join(song_rows) + "\n")

def populate_performer_data(filename, delimiter):
    with open(filename, 'a') as f:
        for performer in performers:
            performer_rows = performer.split("^")
            f.write(delimiter.join(performer_rows) + "\n")

def populate_album_data(filename, delimiter):
    with open(filename, 'a') as f:
        for album in albums:
            album_rows = album.split("^")
            f.write(delimiter.join(album_rows) + "\n")



################################################################################

if __name__ == '__main__':
    # list of producers to read for crawling; could also import
    producer_list = open("producer_list_hb_run_2.txt")

    # file headers
    producer_columns = ["producer_id", "producer_name", "producer_img_url"]
    events_columns = ["producer_id", "performer_id", "song_id", "album_id"]
    produce_song_columns = ["song_id", "song_title", "album_id", "album_title", 
                    "cover_art_url", "performer_id", "performer_name", 
                    "performer_img_url", "song_release_date", "song_release_year", 
                    "song_release_month", "song_release_day", "apple_music_player_url",
                    "producer_id"]
    song_columns = ["song_id", "song_title", "song_release_date", 
                    "song_release_year", "song_release_month", 
                    "song_release_day", "apple_music_player_url"]
    performer_columns = ["performer_id", "performer_name",
                         "performer_img_url"]
    album_columns = ["album_id", "album_title", "cover_art_url", 
                     "album_release_year", "album_release_month",
                     "album_release_day"]

    producer_name_exceptions = {
                                "Menace\n": "639900",
                                "WondaGurl\n": "50896",
                                "Missy Elliott\n": "1529",
                                "Bongo\n": "283439",
                                "The Heatmakerz\n": "27663", 
                                "!llmind\n": "10418", 
                                "1500 or Nothin'\n": "33494", 
                                "Lamar Edwards\n": "73934"
                            }


    # create and write to csvs & text files; csvs for better view of txt python will use
    write_headers("producer_data_hb_run_2.txt", producer_columns, "|")
    write_headers("producer_data_hb_run_2.csv", producer_columns, ",")

    write_headers("events_data_hb_run_2.txt", events_columns, "|")
    write_headers("events_data_hb_run_2.csv", events_columns, ",")

    write_headers("produce_song_data_hb_run_2.txt", produce_song_columns, "|")
    write_headers("produce_song_data_hb_run_2.csv", produce_song_columns, ",")

    write_headers("song_data_hb_run_2.txt", song_columns, "|")
    write_headers("song_data_hb_run_2.csv", song_columns, ",")

    write_headers("performer_data_hb_run_2.txt", performer_columns, "|")
    write_headers("performer_data_hb_run_2.csv", performer_columns, ",")

    write_headers("album_data_hb_run_2.txt", album_columns, "|")
    write_headers("album_data_hb_run_2.csv", album_columns, ",")

    # producer data
    for producer in producer_list:
        # producer name populated from provided list
        producer_name = producer
        # do not start data gathering process unless artist search returns hits            
        if producer_name in producer_name_exceptions:
            producer_id = producer_name_exceptions[producer_name]

            producer_data = get_producer_data(producer_id)
            songs_by_producer_urls = get_songs_url_list(producer_id)

            events = get_events_data(producer_id, songs_by_producer_urls)
            produce_songs = get_produce_song_data(producer_id, songs_by_producer_urls)
            songs = get_song_data(songs_by_producer_urls)
            performers = get_performer_data(songs_by_producer_urls)
            albums = get_album_data(songs_by_producer_urls)

            # gather and populate csv and txt files with producer and song data
            populate_producer_data("producer_data_hb_run_2.txt", "|")
            populate_producer_data("producer_data_hb_run_2.csv", ",")

            populate_events_data("events_data_hb_run_2.txt", "|")
            populate_events_data("events_data_hb_run_2.csv", ",")

            populate_produce_song_data("produce_song_data_hb_run_2.txt", "|")
            populate_produce_song_data("produce_song_data_hb_run_2.csv", ",")

            populate_song_data("song_data_hb_run_2.txt", "|")
            populate_song_data("song_data_hb_run_2.csv", ",")

            populate_performer_data("performer_data_hb_run_2.txt", "|")
            populate_performer_data("performer_data_hb_run_2.csv", ",")

            populate_album_data("album_data_hb_run_2.txt", "|")
            populate_album_data("album_data_hb_run_2.csv", ",")

            # print song to console for progress tracking
            for s in songs:
                print(s)

        elif get_producer_id(producer_name) != "id not found":
            producer_id = get_producer_id(producer_name)

            producer_data = get_producer_data(producer_id)
            songs_by_producer_urls = get_songs_url_list(producer_id)

            events = get_events_data(producer_id, songs_by_producer_urls)
            produce_songs = get_produce_song_data(producer_id, songs_by_producer_urls)
            songs = get_song_data(songs_by_producer_urls)
            performers = get_performer_data(songs_by_producer_urls)
            albums = get_album_data(songs_by_producer_urls)

            # gather and populate csv and txt files with producer and song data
            populate_producer_data("producer_data_hb_run_2.txt", "|")
            populate_producer_data("producer_data_hb_run_2.csv", ",")

            populate_events_data("events_data_hb_run_2.txt", "|")
            populate_events_data("events_data_hb_run_2.csv", ",")

            populate_produce_song_data("produce_song_data_hb_run_2.txt", "|")
            populate_produce_song_data("produce_song_data_hb_run_2.csv", ",")

            populate_song_data("song_data_hb_run_2.txt", "|")
            populate_song_data("song_data_hb_run_2.csv", ",")

            populate_performer_data("performer_data_hb_run_2.txt", "|")
            populate_performer_data("performer_data_hb_run_2.csv", ",")

            populate_album_data("album_data_hb_run_2.txt", "|")
            populate_album_data("album_data_hb_run_2.csv", ",")

            # print song to console for progress tracking
            for s in songs:
                print(s)





