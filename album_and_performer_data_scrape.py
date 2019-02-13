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
        album_title = j['response']['album']['name']
        
        if j['response']['album']['cover_art_url']:
            album_art_url = j['response']['album']['cover_art_url']
        else:
            album_art_url = ""

        if j['response']['album']['cover_art_url']['release_date']:
            release_date = j['response']['album']['cover_art_url']['release_date']
        else:
            release_date = ""

        if j['response']['album']['cover_art_url']['release_date_components']['year']:
            release_year = j['response']['album']['cover_art_url']['release_date_components']['year']
        else: 
            release_year = ""

        if j['response']['album']['cover_art_url']['release_date_components']['month']:
            release_month = j['response']['album']['cover_art_url']['release_date_components']['year']
        else:
            release_month = ""

        if j['response']['album']['cover_art_url']['release_date_components']['day']:
            release_day = j['response']['album']['cover_art_url']['release_date_components']['day']
        else:
            release_day = ""


        album_data.append(songs.append(f"{album_id}^{album_title}^{album_art_url}^{release_date}^{release_year}^{release_month}^{release_day}"))

    return album_data


def get_performer_data(): 
    performer_data = []

    for line in performer_id_list:
        r = requests.get(ALBUM_URL + line)
        j = r.json()

        performer_id = line
        performer_name = j['response']['artist']['name']
        
        if j['response']['artist']['image_url']:
            performer_img_url = j['response']['album']['cover_art_url']
        else:
            performer_img_url = ""

        if j['response']['artist']['description_preview']:
            bio = j['response']['artist']['description_preview']
        else:
            bio = ""

        performer_data.append(songs.append(f"{performer_id}^{performer_name}^{performer_img_url}^{bio}"))

    return performer_data



################################################################################

if __name__ == '__main__':
    # refernce list of producers to read for crawling (could also import @ top)
    album_id_list = open("album_ids.txt")
    performer_id_list = open("performer_ids.txt")

    # create and write to csvs & text files; csvs for better view of txt python will use
    # producer data
    with open('album_data.txt', 'w') as f:
        f.write("album_id, album_name, release_date, release_year, release_month, release_day, album_art_url, apple_music_player_url\n")

    with open('album_data.csv', 'w') as f:
        f.write("album_id, album_name, release_date, release_year, release_month, release_day, album_art_url, apple_music_player_url\n")    

    with open('performer_data.txt', 'w') as f:
        f.write("performer_id, performer_name, performer_img_url, bio\n")

    with open('performer_data.csv', 'w') as f:
        f.write("performer_id, performer_name, performer_img_url, bio\n")

    album_data_list = get_album_data()

    with open('album_data.txt', 'a') as f:
        for data in album_data_list():
            album_data_components = data.split("^")
            f.write(
                str(album_data_components[0]) + "|" + 
                str(album_data_components[1]) + "|" + 
                str(album_data_components[2]) + "|" + 
                str(album_data_components[3]) + "|" +
                str(album_data_components[4]) + "|" + 
                str(album_data_components[5]) + "|" + 
                str(album_data_components[6]) + "|" + 
                str(album_data_components[7]) +
                "\n"
            )

    with open('album_data.csv', 'a') as f:
        for data in album_data_list():
            album_data_components = data.split("^")
            f.write(
                str(album_data_components[0]) + "," + 
                str(album_data_components[1]) + "," + 
                str(album_data_components[2]) + "," + 
                str(album_data_components[3]) + "," +
                str(album_data_components[4]) + "," + 
                str(album_data_components[5]) + "," + 
                str(album_data_components[6]) + "," + 
                str(album_data_components[7]) +
                "\n"
            )

    with open('album_data.txt', 'a') as f:
        for data in performer_data_list():
            performer_data_components = data.split("^")
            f.write(
                str(performer_data_components[0]) + "|" + 
                str(performer_data_components[1]) + "|" + 
                str(performer_data_components[2]) + "|" + 
                str(performer_data_components[3]) + "|" +
                str(performer_data_components[4]) + "|" + 
                str(performer_data_components[5]) + "|" + 
                str(performer_data_components[6]) + "|" + 
                str(performer_data_components[7]) +
                "\n"
            )

    with open('album_data.csv', 'a') as f:
        for data in performer_data_list():
                album_data_components = data.split("^")
                f.write(
                    str(performer_data_components[0]) + "," + 
                    str(performer_data_components[1]) + "," + 
                    str(performer_data_components[2]) + "," + 
                    str(performer_data_components[3]) + "," +
                    str(performer_data_components[4]) + "," + 
                    str(performer_data_components[5]) + "," + 
                    str(performer_data_components[6]) + "," + 
                    str(performer_data_components[7]) +
                    "\n"
                )







