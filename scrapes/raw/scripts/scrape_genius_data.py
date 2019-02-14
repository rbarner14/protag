import sys
import requests 
import time



SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
SONG_URL = "https://genius.com/api/songs/"
PERFOMER_URL = "https://genius.com/api/songs/"
ALBUM_URL = "https://genius.com/api/albums/"

# refactor to add things to dictionary list; create it to a json
# figure out how to re

def get_songs_url_list(producer_id):

    for i in range(32):
        song_url = SONGS_URL % (producer_id, i+1)
        songs_by_producer_urls.append(song_url)

    print(songs_by_producer_urls)

  
def get_producer_id(producer_name):

    url = SEARCH_URL + producer_name

    print(url)

    r = requests.get(url)
    j = r.json()

    for section in j['response']['sections']:
        if section['type'] == 'artist':
            producer_id = section['hits'][0]['result']['id']
            break

    return producer_id

def get_genius_producer_name(producer_name):

    url = SEARCH_URL + producer_name

    print(url)

    r = requests.get(url)
    j = r.json()

    for section in j['response']['sections']:
        if section['type'] == 'artist':
            genius_producer_name = section['hits'][0]['result']['name'].rstrip()
            break

    return genius_producer_name 

def get_producer_image_url(producer_name):

    url = SEARCH_URL + producer_name

    r = requests.get(url)
    j = r.json()

    for section in j['response']['sections']:
        if section['type'] == 'artist':
            producer_image_url = section['hits'][0]['result']['image_url'].rstrip()
            break

    return producer_image_url 

def get_song_data(producer_id):

    songs = []
    song_urls = []

    for url in songs_by_producer_urls:
        print(url)

        r = requests.get(url)
        j = r.json()


        for song in j['response']['songs']: 
            song_id = song['id']
            song_url = SONG_URL + str(song_id)
            song_urls.append(song_url)

        time.sleep(1)


    for url in song_urls:
        print(url)

        r2 = requests.get(url)
        j2 = r2.json()

        if j2['response']['song']['id'] != None: 
            song_id = j2['response']['song']['id']
        else: 
            song_id = ""

        if j2['response']['song']['title'] != None:
            song_title = j2['response']['song']['title'].rstrip()
        else: 
            song_title = ""

        if j2['response']['song']['release_date'] != None:
            release_date = j2['response']['song']['release_date'].rstrip()
        else:
            release_date = ""

        if j2['response']['song']['apple_music_player_url'] != None:
            apple_music_player_url = j2['response']['song']['apple_music_player_url'].rstrip()
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
            
        # songs.append(f"{song_id}|{song_title}|{performer_id}|{album_id}|{release_date}|{release_year}|{release_month}|{release_day}|{apple_music_player_url}")
        songs.append(f"{song_id}^{song_title}^{album_id}^{performer_id}^{release_date}^{release_year}^{release_month}^{release_day}^{apple_music_player_url}")

        # songs.append(f"{song_title}|{album_id}|{song_title}|{song_title}|{song_title}|{song_title}|{song_title}|{song_title}|{song_title}")

        time.sleep(1)

    return songs

################################################################################

if __name__ == '__main__':
    producer_list = open("producer_list_all.txt")

    with open('producer_data_scrape_txt_all.txt', 'w') as f:
        f.write("artist_id, producer_name, producer_img_url\n")

    with open('producer_data_scrape_csv_all.csv', 'w') as f:
        f.write("artist_id, producer_name, producer_img_url\n")

    with open('song_data_scrape_txt_all.txt', 'w') as f:
        f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")

    with open('song_data_scrape_csv_all.csv', 'w') as f:
        f.write("song_id, song_title, album_id, performer_id, release_date, release_year, release_month, release_day, apple_music_player_url\n")

    for producer in producer_list:

        producer_name = producer
        genius_producer_name = get_genius_producer_name(producer_name)
        producer_id = get_producer_id(producer_name)
        producer_image_url = get_producer_image_url(producer_name)
        songs_by_producer_urls = []

        get_songs_url_list(producer_id)

        songs = get_song_data(producer_id)


        with open('producer_data_scrape_txt_all.txt', 'a') as f:
            f.write(
                str(producer_id) + " | " + genius_producer_name + " | " + 
                producer_image_url +
                "\n"
            )

        with open('producer_data_scrape_csv_all.csv', 'a') as f:
            f.write(
                str(producer_id) + " , " + genius_producer_name + " , " + 
                producer_image_url +
                "\n"
            )

        with open('song_data_scrape_txt_all.txt', 'a') as f:
            for song in songs:
                split_songs = song.split("^")
                f.write(
                    str(split_songs[0]) + " | " + str(split_songs[1]) + " | " + 
                    str(split_songs[2]) + " | " + str(split_songs[3]) + " | " +
                    str(split_songs[4]) + " | " + str(split_songs[5]) + " | " +
                    str(split_songs[6]) + " | " + str(split_songs[7]) + " | " +
                    str(split_songs[8]) + 
                    "\n"
                )

        with open('song_data_scrape_csv_all.csv', 'a') as f:
            for song in songs:
                split_songs = song.split("^")
                f.write(
                    str(split_songs[0]) + " , " + str(split_songs[1]) + " , " + 
                    str(split_songs[2]) + " , " + str(split_songs[3]) + " , " +
                    str(split_songs[4]) + " , " + str(split_songs[5]) + " , " +
                    str(split_songs[6]) + " , " + str(split_songs[7]) + " , " +
                    str(split_songs[8]) +
                    "\n"
                )

        for s in songs:
            print(s)



