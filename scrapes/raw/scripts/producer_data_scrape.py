import sys # for running search at command line; may not be needed
import time # for sleeping

import requests # for get requests


SEARCH_URL = "https://genius.com/api/search/artist?page=1&q=" 
SONGS_URL = "https://genius.com/api/artists/%s/songs?page=%s&sort=popularity"
ARTIST_URL = "https://genius.com/api/artists/"

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

        producer_data.append(f"{genius_producer_name}^{producer_image_url}")

    return producer_data


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


################################################################################

if __name__ == '__main__':
    # list of producers to read for crawling; could also import
    producer_list = open("producer_list.txt")

    # file headers
    producer_columns = ["producer_id", "producer_name", "producer_img_url"]

    # create and write to csvs & text files; csvs for better view of txt python will use
    write_headers("producer_data.txt", producer_columns, "|")
    write_headers("producer_data.csv", producer_columns, ",")

    # # producer data
    for producer in producer_list:
        # producer name populated from provided list
        producer_name = producer

    #     # do not start data gathering process unless artist search returns hits
        if get_producer_id(producer_name) != "id not found":
            producer_id = get_producer_id(producer_name)
            producer_data = get_producer_data(producer_name)

            populate_producer_data("producer_data.txt", "|")
            populate_producer_data("producer_data.csv", ",")
            
        time.sleep(1)
