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

@app.route("/search_result")
def return_search_result():

        search_str = request.form.get("search_str")

        results = Song.query.filter(song_title=search_str).all()

        return render_template("search_result.html",results=results)



# @app.route("/get-user-search", methods=["POST"])
# def get_user_search():

#     # Get the name that the user submitted (from request.args).
#     song_name = request.args.get("song_title")
#     producer_name = request.args.get("producer_name")
#     performer_name = request.args.get("performer_name")

#     if song_name: 
#         return render_template("search_result.html");
#     elif producer_name:
#         return render_template("producer_page.html");
#     elif performer_name:
#         return render_template("performer_page.html");

# @app.route("/songs")
# def songs():
#     """Show list of movies."""

#     search_results = (db.session
#               .query(ProduceSong)
#               .join(Songs)
#               .group_by(Songs.song_title)
#               .filter(Songs.song_title == search_str)
#               .all())
    
#     return render_template("search_list.html", search_results=search_results)


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















