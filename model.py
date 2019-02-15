"""Models and database functions for makingmusic db."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Compose ORM
# relying on Genius' ids

class Producer(db.Model):
    """Producer model."""

    __tablename__ = "producers"

    # primary keys are inherently unique
    producer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    producer_name = db.Column(db.String(50), nullable=False)
    producer_img_url = db.Column(db.Text, nullable=True)

    songs = db.relationship("Song", secondary="produce_songs", backref="producers")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Producer producer_id={self.producer_id} producer_name={self.producer_name} producer_img_url={self.producer_img_url}>" # pyflakes does not like f-string; it prefers .format()

    @classmethod
    def get_producer_songs(cls, producer_name):

        return cls.query.filter(cls.producer_name == producer_name).options(db.joinedload("songs")).first()


class Performer(db.Model):
    """Performer model."""

    __tablename__ = "performers"

    performer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    performer_name = db.Column(db.String(50), nullable=False)
    performer_img_url = db.Column(db.Text, nullable=True)

    songs = db.relationship("Song", secondary="produce_songs", backref="performers")

    def __repr__(self):

        return f"<Performer performer_id={self.performer_id} performer_name={self.performer_name} performer_img_url={self.performer_img_url}>"

    @classmethod
    def get_performer_songs(cls, performer_name):

    return cls.query.filter(cls.performer_name == performer_name).options(db.joinedload("songs")).first()


class Song(db.Model):
    """Song model."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, nullable=False, primary_key=True)
    song_title = db.Column(db.String(50), nullable=False)
    apple_music_player_url = db.Column(db.Text, nullable=True)
    song_release_date = db.Column(db.DateTime, nullable=True)
    song_release_year = db.Column(db.DateTime, nullable=True)
    song_release_month = db.Column(db.DateTime, nullable=True)
    song_release_day = db.Column(db.DateTime, nullable=True)

    producers = db.relationship("Producer", secondary="produce_songs", backref="songs")

    def __repr__(self):

        return f"<Song song_id={self.song_id} song_title={self.song_title} apple_music_player_url={self.apple_music_player_url} song_release_date={self.song_release_date} song_release_year={self.song_release_year} song_release_month={self.song_release_month} song_release_day={self.song_release_day}>"

    @classmethod
    def get_song_producers(cls, song_title):

        return cls.query.filter(cls.song_title == song_title).options(db.joinedload("producers")).all()

class Album(db.Model):
    """Album model."""

    __tablename__ = "albums"

    album_id = db.Column(db.Integer, nullable=False, primary_key=True)
    album_title = db.Column(db.String(50), nullable=False)
    album_art_url = db.Column(db.Text, nullable=True)
    album_release_date = db.Column(db.DateTime, nullable=True)
    album_release_year = db.Column(db.DateTime, nullable=True)
    album_release_month = db.Column(db.DateTime, nullable=True)
    album_release_day = db.Column(db.DateTime, nullable=True)

    producers = db.relationship("Producer", secondary="produce_songs", backref="albums")

    def __repr__(self):

        return f"<Album album_id={self.album_id} album_title={self.album_title} album_art_url={self.album_art_url} release_date={self.release_date} release_year={self.release_year} release_month={self.release_month} release_day={self.release_day}>"

    @classmethod
    def get_album_producers(cls, album_title):

        return cls.query.filter(cls.album_title == album_title).options(db.joinedload("producers")).all()

class ProduceSong(db.Model):
    """ProduceSong model."""

    __tablename__ = "produce_songs"

    event_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.producer_id'), nullable=False)
    performer_id = db.Column(db.Integer, db.ForeignKey('performers.performer_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'), nullable=True)

    def __repr__(self):

        return f"<ProduceSong event_id={self.event_id} producer_id={self.producer_id} performer_id={self.performer_id} song_id={self.song_id} album_id={self.album_id}>"

# may add Users class in 3.0

##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///animals'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
