import sys
import requests
import time

SEARCH_URL = "https://genius.com/api/search/artist?page=1&q="
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=1&sort=popularity"


def get_artist_id(artist_name):

  url = SEARCH_URL + artist_name

  print(url)

  r = requests.get(url)
  j = r.json()

  for section in j['response']['sections']:
    if section['type'] == 'artist':
        break

  return section['hits'][0]['result']['id']  


def get_songs(artist_id):

  url = SONGS_URL % artist_id

  print(url)

  r = requests.get(url)
  j = r.json()

  songs = []

  for song in j['response']['songs']:
    songs.append(song['title'])

  return songs


if __name__ == '__main__':

  artist_name = sys.argv[1]
  artist_id = get_artist_id(artist_name)
  songs = get_songs(artist_id)

  for s in songs:
    print(s)
