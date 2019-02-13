"""Models and database functions for makingmusic db."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Compose ORM

class Producer(db.Model):
    """Producer model."""

    __tablename__ = "producers"

    producer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    producer_name = db.Column(db.String(25), nullable=False)
    img_url = db.Column(db.Text, nullable=True) # DOUBLE CHECK THIS
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Producer producer_id={self.producer_id} producer_name={self.producer_name} img_url={self.img_url} bio={self.bio}>" # pyflakes does not like f-string; it prefers .format()


class Song(db.Model):
    """Animal model."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    song_name = db.Column(db.Integer, db.ForeignKey('humans.human_id'), nullable=False)
    media_url = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    release_year = db.Column(db.DateTime, nullable=True)
    release_month = db.Column(db.DateTime, nullable=True)
    release_day = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Song song_id={self.song_id} song_name={self.song_name} media_url={self.media_url} release_date={self.release_date} release_year={self.release_year} release_month={self.release_month} release_day={self.release_day}>"


class Song(db.Model):
    """Animal model."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    song_name = db.Column(db.Integer, db.ForeignKey('humans.human_id'), nullable=False)
    media_url = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    release_year = db.Column(db.DateTime, nullable=True)
    release_month = db.Column(db.DateTime, nullable=True)
    release_day = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Song song_id={self.song_id} song_name={self.song_name} media_url={self.media_url} release_date={self.release_date} release_year={self.release_year} release_month={self.release_month} release_day={self.release_day}>"




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
