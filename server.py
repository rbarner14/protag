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


@app.route("/get-user-search", methods=["POST"])
def get_user_search():

    # Get the name that the user submitted (from request.args).
    song_name = request.args.get("song_title")
    producer_name = request.args.get("producer_name")
    performer_name = request.args.get("performer_name")

    if song_name: 
        return render_template("search_result.html");
    elif producer_name:
        return render_template("producer_page.html");
    elif performer_name:
        return render_template("performer_page.html");

@app.route("/producer/<int:producer_name>", methods=["GET"])



if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
