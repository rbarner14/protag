import datetime
from sqlalchemy import func

from model import Producer, Performer, Song, Album, ProduceSong
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
        performer_id, producer_name, performer_img_url = row.split("|")

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
        song_id, song_title, song_release_date, song_release_year, song_release_month, song_release_day, apple_music_player_url = row.split("|")

        # The date is in the file as string; this converts it to an actual 
        # datetime object.
        

        song = Performer(song_id=song_id, 
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
        album_id, album_title, cover_art_url, album_release_year, album_release_month, album_release_day = row.split("|")

        album = Performer(album_id=album_id, 
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
        producer_id, perfomer_id, song_id, album_id = row.split("|")

        song = Performer(producer_id=producer_id, 
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
    performers_filename = "seed_data/performers.txt"
    songs_filename = "seed_data/songs.txt"
    albums_filename = "seed_data/albums.txt"
    events_filename = "seed_data/events.txt"
    load_producers(producer_filename)
    load_performers(performer_filename)
    load_songs(song_filename)
    load_albums(album_filename)
    load_events(event_filename)
