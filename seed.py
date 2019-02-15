import datetime
from sqlalchemy import func # will use when adding log-in functionality

from model import Producer, Performer, Song, Album, ProduceSong, connect_to_db, db
from server import app

def load_producers(producer_filename):
    """Load producers from producers.txt into database."""

    print("Producers")

    # Complete the for loop defined for every line in producer_filename.
    for i, row in enumerate(open(producer_filename)):
        row = row.rstrip()
        producer_id, producer_name, producer_img_url = row.split("|")

        producer = Producer(producer_id=producer_id,
                    producer_name=producer_name,
                    producer_img_url=producer_img_url)

        # add to the session
        db.session.add(producer)

        # Provided for progress tracking (print every 10 lines).
        if i % 10 == 0:
            print(i)

    # Once data table is built, commit it to the database.
    db.session.commit()


def load_performers(performer_filename):
    """Load performers from performers.txt into database."""

    print("Performers")

    for i, row in enumerate(open(performer_filename)):
        row = row.rstrip()
        performer_id, performer_name, performer_img_url = row.split("|")

        performer = Performer(performer_id=performer_id,
                    performer_name=performer_name,
                    performer_img_url=performer_img_url)

        db.session.add(performer)

        if i % 10 == 0:
            print(i)

    db.session.commit()


def load_songs(song_filename):
    """Load songs from songs.txt into database."""

    print("Songs")

    for i, row in enumerate(open(song_filename)):
        row = row.rstrip()
        song_id, song_title, song_release_date_str, song_release_year_str, song_release_month_str, song_release_day_str, apple_music_player_url = row.split("|")

        # The date is in the file as string; this converts it to an actual 
        # datetime object.
        if song_release_date_str and song_release_month_str not in("None", "None""):
            song_release_date = datetime.datetime.strptime(song_release_date_str, "%Y-%m-%d")
        else:
            song_release_date = None

        if song_release_year_str and song_release_year_str not in("None", "None""):
            song_release_year = datetime.datetime.strptime(song_release_year_str, "%Y")
        else:
            song_release_year = None

        if song_release_month_str and song_release_month_str not in("None", "None""):
            song_release_month = datetime.datetime.strptime(song_release_month_str, "%m")
        else:
            song_release_month = None

        if song_release_day_str and song_release_day_str not in("None", "None""):
            if len(song_release_day_str) == 1:
                song_release_day_new = "0" + song_release_day_str
                song_release_day = datetime.datetime.strptime(song_release_day_new, "%d")
            else:
                song_release_day = datetime.datetime.strptime(song_release_day_str, "%d")
        else: 
            song_release_day = None

        song = Song(song_id=song_id, 
                song_title=song_title, 
                song_release_date=song_release_date, 
                song_release_year=song_release_year, 
                song_release_month=song_release_month, 
                song_release_day=song_release_day, 
                apple_music_player_url=apple_music_player_url)

        db.session.add(song)

        if i % 1000 == 0:
            print(i)

            # An optimization: if commit after every add, the database
            # will do a lot of work committing each record. However,
            # waiting until the end may be quite the load on computers with 
            # smaller amounts of memory; it might thrash around. Committing 
            # every 1,000th add is a good balance.
            db.session.commit()

    db.session.commit()


def load_albums(album_filename):
    """Load albums from albums.txt into database."""

    print("Albums")

    for i, row in enumerate(open(album_filename)):
        row = row.rstrip()
        album_id, album_title, cover_art_url, album_release_year_str, album_release_month_str, album_release_day_str = row.split("|")

        if album_release_year_str and album_release_year_str not in("None", "None""):
            album_release_year = datetime.datetime.strptime(album_release_year_str, "%Y")
        else:
            album_release_year = None

        if album_release_month_str and album_release_month_str not in("None", "None""):
            album_release_month = datetime.datetime.strptime(album_release_month_str, "%m")
        else:
            album_release_month = None

        if album_release_day_str and album_release_day_str not in("None", "None""):
            if len(album_release_day_str) == 1:
                album_release_day_str = "0" + album_release_day_str
                album_release_day = datetime.datetime.strptime(album_release_day_str, "%d")
            else:
                album_release_day = datetime.datetime.strptime(album_release_day_str, "%d")
        else: 
            album_release_day = None


        album = Album(album_id=album_id, 
                album_title=album_title, 
                cover_art_url=cover_art_url, 
                album_release_year=album_release_year, 
                album_release_month=album_release_month, 
                album_release_day=album_release_day)

        db.session.add(album)

        if i % 500 == 0:
            print(i)

            db.session.commit()

    db.session.commit()


def load_events(event_filename):
    """Load events from events.txt into database."""

    print("Events")

    for i, row in enumerate(open(event_filename)):
        row = row.rstrip()
        producer_id, performer_id, song_id, album_id = row.split("|")

        song = ProduceSong(producer_id=producer_id, 
                performer_id=performer_id, 
                song_id=song_id, 
                album_id=album_id)

        db.session.add(song)

        if i % 1000 == 0:
            print(i)

            db.session.commit()

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    producer_filename = "seed_data/producers.txt"
    performer_filename = "seed_data/performers.txt"
    song_filename = "seed_data/songs.txt"
    album_filename = "seed_data/albums.txt"
    event_filename = "seed_data/events.txt"
    load_producers(producer_filename)
    load_performers(performer_filename)
    load_songs(song_filename)
    load_albums(album_filename)
    load_events(event_filename)
