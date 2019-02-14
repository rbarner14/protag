import requests
import time


ALBUM_URL = "https://genius/com/api/albums/"
ARTIST_URL = "https://genius/com/api/albums/"

# 
def get_album_data(): 
    album_data = []

    for line in album_id_list:
        r = requests.get(ALBUM_URL + line)
        j = r.json()
        album_id = line
        album = j['response']['album']
        album_title = album['name']
        album_art_url = album['cover_art_url']
        release_date = album['release_date']
        release_date_components = album['release_date_components']

        if release_date != None:
            release_date = release_date_components.get('year', "")
        else: 
            release_date = ""

        if album['release_date_components'] != None:
            release_date_components = album.get('release_date_components', "")
        else: 
            release_date_components = ""

        if release_date_components['year'] != None:
            release_year = release_date_components.get('year', "")
        else:
            release_year = ""

        if release_date_components['month'] != None:
            release_month = release_date_components.get('month', "")
        else:
            release_month = ""

        if release_date_components['day'] != None:
            release_day = release_date_components.get('day', "")

        album_data.append(songs.append(f"{album_id}^{album_title}^{album_art_url}^{release_date}^{release_year}^{release_month}^{release_day}"))

        time.sleep(1)

    return album_data


def get_performer_data(): 
    performer_data = []

    for line in performer_id_list:
        r = requests.get(ALBUM_URL + line)
        j = r.json()

        performer_id = line
        performer = j['response']['artist']
        performer_name = performer['name']
        performer_img_url = performer['image_url']
        
        if performer['img_url'] != None:
            performer_img_url = performer.get('image_url', "")
        else:
            performer_img_url = ""

        performer_data.append(songs.append(f"{performer_id}^{performer_name}^{performer_img_url}"))

        time.sleep(1)
    return performer_data


 # create files and write headers to them
def write_headers(filename, headers, delimiter):
        # w = write to new file
    with open(filename, 'w') as f:
        f.write(delimiter.join(headers)+ "\n")

# append ('a') data to producer file already created
def populate_album_data(filename, delimiter):
    with open(filename, 'a') as f:
        for data in album_data_list:
            album_data_components = data.split("^")
            f.write(delimiter.join(album_data_components) + "\n")

# append ('a') data to song file already created
def populate_performer_data(filename, delimiter):
    with open(filename, 'a') as f:
        for data in performer_data_list:
            performer_data_components = data.split("^")
            f.write(delimiter.join(performer_data_components) + "\n")

################################################################################

if __name__ == '__main__':
    # refernce list of producers to read for crawling (could also import @ top)
    album_id_list = open("album_id_list.txt")
    performer_id_list = open("performer_id_list.txt")

    album_columns = ["album_id, album_name", "release_date", "release_year", 
                     "release_month", "release_day", "album_art_url", 
                     "apple_music_player_url"]
    performer_columns = ["performer_id", "performer_name", "performer_img_url"]

    # create and write to csvs & text files; csvs for better view of txt python 
    # will use producer data

    album_data_list = get_album_data()
    performer_data_list = get_performer_data()

    populate_album_data("album_data.txt", "|")
    populate_album_data("album_data.csv", ",")
    populate_performer_data("perfomer_data.txt", "|")
    populate_performer_data("perfomer_data.csv", ",")

    # with open('album_data.txt', 'a') as f:
    #     for data in album_data_list:
    #         album_data_components = data.split("^")
    #         f.write(
    #             str(album_data_components[0]) + "|" + 
    #             str(album_data_components[1]) + "|" + 
    #             str(album_data_components[2]) + "|" + 
    #             str(album_data_components[3]) + "|" +
    #             str(album_data_components[4]) + "|" + 
    #             str(album_data_components[5]) + "|" + 
    #             str(album_data_components[6]) + "|" + 
    #             str(album_data_components[7]) +
    #             "\n"
    #         )

    # with open('album_data.csv', 'a') as f:
    #     for data in album_data_list:
    #         album_data_components = data.split("^")
    #         f.write(
    #             str(album_data_components[0]) + "," + 
    #             str(album_data_components[1]) + "," + 
    #             str(album_data_components[2]) + "," + 
    #             str(album_data_components[3]) + "," +
    #             str(album_data_components[4]) + "," + 
    #             str(album_data_components[5]) + "," + 
    #             str(album_data_components[6]) + "," + 
    #             str(album_data_components[7]) +
    #             "\n"
    #         )

    # with open('album_data.txt', 'a') as f:
    #     for data in performer_data_list:
    #         performer_data_components = data.split("^")
    #         f.write(
    #             str(performer_data_components[0]) + "|" + 
    #             str(performer_data_components[1]) + "|" + 
    #             str(performer_data_components[2]) + "|" + 
    #             str(performer_data_components[3]) + "|" +
    #             str(performer_data_components[4]) + "|" + 
    #             str(performer_data_components[5]) + "|" + 
    #             str(performer_data_components[6]) + "|" + 
    #             str(performer_data_components[7]) +
    #             "\n"
    #         )

    # with open('album_data.csv', 'a') as f:
    #     for data in performer_data_list:
    #             album_data_components = data.split("^")
    #             f.write(
    #                 str(performer_data_components[0]) + "," + 
    #                 str(performer_data_components[1]) + "," + 
    #                 str(performer_data_components[2]) + "," + 
    #                 str(performer_data_components[3]) + "," +
    #                 str(performer_data_components[4]) + "," + 
    #                 str(performer_data_components[5]) + "," + 
    #                 str(performer_data_components[6]) + "," + 
    #                 str(performer_data_components[7]) +
    #                 "\n"







