import datetime
from sqlalchemy import func

from model import Producer, Performer, Song, Album, ProduceSong
from server import app

def load_producers(producer_filename):
    """Load producers from m.producers into database"""

    print("Producers")

    # complete the for loop defined for every line in producer_filename
    for i, row in enumerate(open(producer_filename)):
        row = row.rstrip()
        producer_id, producer_name, producer_img_url = row.split("|")

        producer = Producer(producer_id=producer_id,
                    producer_name=producer_name,
                    producer_img_url=producer_img_url)

        # add to the session
        db.session.add(producer)

        # provided for progress tracking (print every 10 lines)
        if i % 10 == 0:
            print(i)

    # once data table is built, commit it to the database
    db.session.commit()


def load_performers(performer_filename):
    """Load performers from m.performers into database"""

    print("Performers")

    # complete the for loop defined for every line in producer_filename
    for i, row in enumerate(open(performer_filename)):
        row = row.rstrip()
        performer_id, producer_name, performer_img_url = row.split("|")

        performer = Performer(producer_id=producer_id,
                    producer_name=producer_name,
                    producer_img_url=producer_img_url)

        # add to the session
        db.session.add(producer)

        # provided for progress tracking (print every 10 lines)
        if i % 10 == 0:
            print(i)

    # once data table is built, commit it to the database
    db.session.commit()


def load_albums(album_filename):


def load_songs(song_filename):


def load_events(event_filename):