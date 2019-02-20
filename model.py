"""Models and database functions for music db."""

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

    # establish relationships
    # the Producer class has an albums attribute that is a list of Album objects 
    # using the relationship defined and "produce_song" as the association table 
    # attributes are plural to communicate cardinaltiy: a Producer can have 
    # many songs and albums
    songs = db.relationship("Song", secondary="produce_songs", backref="producers")
    albums = db.relationship("Album", secondary="produce_songs", backref="producers")

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
    albums = db.relationship("Album", secondary="produce_songs", backref="performers")

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
    cover_art_url = db.Column(db.Text, nullable=True)
    album_release_date = db.Column(db.DateTime, nullable=True)

    songs = db.relationship("Song", secondary="produce_songs", backref="album")

    def __repr__(self):

        # return f"<Album album_id={self.album_id} album_title={self.album_title} cover_art_url={self.cover_art_url} release_year={self.album_release_year} release_month={self.album_release_month} release_day={self.album_release_day}>"
        return f"<Album album_id={self.album_id} album_title={self.album_title} cover_art_url={self.cover_art_url} release_date={self.album_release_date}>"

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

    # because there is only one performer per song, a 1 to 1 relationship is 
    # established with performer
    # ProduceSong has an attribute performer that is a Performer object 
    # using the produce_songs reference (there is a direct relationship) between
    # performer and ProduceSong which is the performer_id
    # performer can have multiple songs
    performer = db.relationship("Performer", backref="events")

    def __repr__(self):

        return f"<ProduceSong event_id={self.event_id} producer_id={self.producer_id} performer_id={self.performer_id} song_id={self.song_id} album_id={self.album_id}>"


# may add Users class in 3.0



##############################################################################

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use database.
    # Creates database when entering psql music at commandline.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///music' 
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Added for module interactive convenience to work directly with database.
    
    from server import app
    connect_to_db(app)
    print("Connected to DB.")






