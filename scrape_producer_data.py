import sys
import requests 
import time
import os



SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
artist_name = "" 
songs_url_list = []


with open('play_results_7_txt.txt', 'w') as f:
  f.write("artist_id, artist_name, song_id, song_title, performer_id, performer_name, artist_img_url, album_art_url\n")

with open('play_results_7_csv.csv', 'w') as g:
  g.write("artist_id, artist_name, song_id, song_title, performer_id, performer_name, artist_img_url, album_art_url\n")



def get_songs_url_list(artist_id):

  for i in range(3):
    song_url = SONGS_URL % (artist_id, i+1)
    songs_url_list.append(song_url)

  print(songs_url_list)

  
def get_artist_id(artist_name):

  url = SEARCH_URL + artist_name

  print(url)

  r = requests.get(url)
  j = r.json()

  for section in j['response']['sections']:
    if section['type'] == 'artist':
        artist_name = section['hits'][0]['result']['name']
        break

  return section['hits'][0]['result']['id']  


def get_songs(artist_id):

  songs = []
  for url in songs_url_list:
    print(url)

    r = requests.get(url)
    j = r.json()


    for song in j['response']['songs']: 
      song_id = song['id']
      song_title = song['title'].rstrip()
      performer_id = song['primary_artist']['id']
      performer_name = song['primary_artist']['name'].rstrip()
      artist_img_url = song['primary_artist']['image_url'].rstrip()
      album_art_url = song['song_art_image_thumbnail_url'].rstrip()

      songs.append(f"{artist_id}|{artist_name}|{song_id}|{song_title}|{performer_id}|{performer_name}|{artist_img_url}|{album_art_url}")
    
    time.sleep(5)

  return songs

################################################################################

if __name__ == '__main__':
  artist_name = sys.argv[1]
  artist_id = get_artist_id(artist_name)

  get_songs_url_list(artist_id)

  songs = get_songs(artist_id)

  with open('play_results_7_txt.txt', 'a') as f:
    for song in songs:
      split_songs = song.split("|")
      f.write(
        str(split_songs[0]) + " | " + str(split_songs[1]) + " | " + 
        str(split_songs[2]) + " | " + str(split_songs[3]) + " | " + 
        str(split_songs[4]) + " | " + str(split_songs[5])+ " | " + 
        str(split_songs[6]) + " | " + str(split_songs[7]) + 
        "\n"
      )

  with open('play_results_7_csv.csv', 'a') as g:
    for song in songs:
      split_songs = song.split("|")
      g.write(
        str(split_songs[0]) + " , " + str(split_songs[1]) + " , " + 
        str(split_songs[2]) + " , " + str(split_songs[3]) + " , " + 
        str(split_songs[4]) + " , " + str(split_songs[5]) + " , " + 
        str(split_songs[6]) + " , " + str(split_songs[7]) + 
        "\n"
      )


  for s in songs:
    print(s)



