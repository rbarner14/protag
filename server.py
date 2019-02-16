from jinja2 import StrictUndefined

from flask import Flask, redirect, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required for Flask sessions and debug toolbar use
app.secret_key = "ABC"


@app.route("/")
def index():

        return render_template("homepage.html")


@app.route("/search_result", methods=['GET'])
def return_search_result():

        search_str = request.args.get("search_str")

        if len(search_str) > 0:
            producers = Producer.query.filter(Producer.producer_name.like('%{}%'.format(search_str))).all()
            performers = Performer.query.filter(Performer.performer_name.like('%{}%'.format(search_str))).all()
            songs = Song.query.filter(Song.song_title.like('%{}%'.format(search_str))).all()
            albums = Album.query.filter(Album.album_title.like('%{}%'.format(search_str))).all()
        else:
            producers = None
            performers = None
            songs = None
            albums = None

        return render_template("search_result.html",
                                producers=producers,
                                performers=performers,
                                songs=songs,
                                albums=albums)


@app.route("/producers")
def producer_list():
    """Show list of movies."""

    producers = Producer.query.order_by('producer_name').all()
    return render_template("producer_list.html", producers=producers)


@app.route("/producers/<int:producer_id>", methods=["GET"])
def producer_detail(producer_id):

    producer = Producer.query.get(producer_id)

    songs = Producer.query.get(producer_id).songs

    return render_template("producer.html",
                            producer=producer, 
                            songs=songs)


if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")















