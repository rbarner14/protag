# for feeding variables to templates
from jinja2 import StrictUndefined

# for helpful debugging
from flask import Flask, redirect, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension

#tables for jquery
from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 

# create Flask app
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

        # search string user enters gathered from the form on the homepage
        search_str = request.args.get("search_str")

        # return the producer(s), performer(s), song(s), and album(s) 
        # that match the search string (not case-sensitive), alphabetized
        if len(search_str) > 0:
            producers = Producer.query.order_by('producer_name').filter(Producer.producer_name.ilike('%{}%'.format(search_str))).all()
            performers = Performer.query.order_by('performer_name').filter(Performer.performer_name.ilike('%{}%'.format(search_str))).all()
            songs = Song.query.order_by('song_title').filter(Song.song_title.ilike('%{}%'.format(search_str))).all()
            albums = Album.query.order_by('album_title').filter(Album.album_title.ilike('%{}%'.format(search_str))).all()
        else:
            producers = None
            performers = None
            songs = None
            albums = None

        return render_template("search_result.html",
                                producers=producers,
                                performers=performers,
                                songs=songs,
                                albums=albums
                               )


@app.route("/producers")
def producer_list():
    """Show list of producers."""

    # query for all producers in database; return results alphabetized
    producers = Producer.query.order_by('producer_name').all()

    return render_template("producer_list.html", producers=producers)


# each producer page's url will include the producer's database id
@app.route("/producers/<int:producer_id>", methods=["GET"])
def producer_detail(producer_id):


    producer = Producer.query.get(producer_id)
    albums = producer.albums # list
    # returns the album release years in descending chronological order
    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    return render_template("producer.html",
                            producer=producer,
                            album_years=album_years
                           )


@app.route("/performers")
def performer_list():
    """Show list of performers."""

    # query for all producers in database; return results alphabetized    
    performers = Performer.query.order_by('performer_name').all()

    return render_template("performer_list.html", performers=performers)


# each performer's page's url will include the performer's database id
@app.route("/performers/<int:performer_id>", methods=["GET"])
def performer_detail(performer_id):

    performer = Performer.query.get(performer_id)

    return render_template("performer.html",
                            performer=performer
                          )


@app.route("/songs")
def song_list():
    """Show list of songs."""

    songs = Song.query.order_by('song_title').all()

    return render_template("song_list.html", 
                            songs=songs
                          )


# each song's page's url will include the song's database id
@app.route("/songs/<int:song_id>", methods=["GET"])
def song_detail(song_id):

    song = Song.query.get(song_id)

    return render_template("song.html",
                            song=song
                           )


@app.route("/albums")
def album_list():
    """Show list of albums."""

    albums = Album.query.order_by('album_title').all()

    return render_template("album_list.html", 
                            albums=albums
                          )

# each album's page's url will include the album's database id
@app.route("/albums/<int:album_id>", methods=["GET"])
def album_detail(album_id):

    album = Album.query.get(album_id)
    
    return render_template("album.html",
                            album=album
                          )


################################################################################

if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")















