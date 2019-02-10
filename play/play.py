#!/usr/bin/env python3

#https://genius.com/api/artists/4617/songs?page=1&sort=popularity
#https://genius.com/api/search/multi?q=the+neptunes
#https://genius.com/api/search/artist?page=1&q=the+neptunes

# import sys library
import sys
# import requests library
import requests

# json representation immitating search from nav bar on any genius page 
# url for this variable concluded from recording search on genius with developer 
# tools' Network section 
SEARCH_URL = "https://genius.com/api/search/artist?page=1&q="
# cleared site data in Application tab
# the page of JSON needed for gathering artists' songs they have produced and 
# the performers of those songs
# %s will be replaced with the artists' name  
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=1&sort=popularity"


# define function get_artist_id takes one argument artist_name that is passed in
# at command line
def get_artist_id(artist_name):
  # the artist_name passed in as an argument is added to the SEARCH_URL variable
  # (str) defined as global variable above
  url = SEARCH_URL + artist_name
  # prints to user the url that is being searched
  print(url)
  # variable r is bound to the variable requests (from the requests library)
  # a get request (read) method is called, passing in the url variable defined
  # here 
  r = requests.get(url)
  # variable j is bound to the result of r with the method json applied to turn 
  # the get request results into a json that can be interpreted by our reader in 
  # browser to facilitate human interpretation
  j = r.json()
  # j['response']['sections'] is a list containing data we need in the json 
  # that is unpacked with a for loop
  for section in j['response']['sections']:
    # conditional is ran:
    # if the type key value in section is "artist"...???
    if section['type'] == 'artist':
        break
  # return the value at key id for the artist id which is the first value in 
  # the hits list; hits refers to "search hits", or the results that returned
  # from the string searched; max # of search results not identified
  return section['hits'][0]['result']['id']  

# function get_songs is defined that takes in a single argument "artist_id"
def get_songs(artist_id):
  # the variable url is bound to the variable SONGS_URL defined above 
  # the %s in the SONGS_URL is replaced by the artist_id passed in this function
  url = SONGS_URL % artist_id
  # the artists' songs url is printed to the console
  print(url)
  # the variable r is bound to the requests method .get() that takes in the url
  # as a parameter (a get request to read content @ url fed in)
  r = requests.get(url)
  # a variable j is defined to jsonfiy the output from the get request defined
  # as r above
  j = r.json()

  # songs is a variable bound to an empty string
  songs = []
  # the list at 
  for song in j['response']['songs']:
    songs.append(song['title'])
  return songs


# runs python at command line without calling functions
# functions defined in python file are not run at command line until 
# search argument is entered in quotes after running file
# can run file with ./play.py "artist name" or python3 play.py "artist name"
if __name__ == '__main__':
  # artist name to feed in get_artist_id function = string argument of artist name 
  # entered when running file at command line
  artist_name = sys.argv[1]
  # artist_id variable is bound to the function call of get_artist_id with the
  # passed in artist_name as a variable
  artist_id = get_artist_id(artist_name)
  # songs variable is bound to the function call of get_songs that takes in the
  # artist_id as a parameter
  songs = get_songs(artist_id)
  # 
  for s in songs:
    print(s)



