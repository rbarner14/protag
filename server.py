from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Getting our list of MOST LOVED MELONS

# YOUR ROUTES GO HERE
@app.route("/")
def index():

    # Check if a name is in the session, and if so, 
    # redirect to the /top-melons route.
    # if 'name' in session:
    #     return redirect("/top-melons")
    # else: 
        return render_template("homepage.html")

# SH: should be POST method
@app.route("/get-user-search", methods=["GET"])
def get_user_search():

    # Get the name that the user submitted (from request.args).
    song_name = request.args.get("songname")
    producer_name = request.args.get("producername")
    performer_name = request.args.get("performername")

    # Add the user’s name to the session.
    # if not name:
        # if we have an existing name in the session, remove it
        # if name in session:
        #     del session['name']
    #     return redirect("/")
    # else: 
    #     session['name'] = name
    if song_name: 
        return render_template("search_result.html");
    elif producer_name:
        return render_template("producer_page.html");
    elif performer_name:
        return render_template("performer_page.html");

    # After the name has been added to the session, 
    # redirect to the /top-melons route.
    # return redirect("/top-melons")


# @app.route("/top-melons")
# def display_most_loved_melons():

#     # Enable Jinja's access to dictionaries in MOST_LOVED_MELONS
#     melons = MOST_LOVED_MELONS.values()
#     username = session.get('name')
    
#     # Check if there is a name stored in the session already. 
#     # If so, render the template top-melons.html. 
#     # If not, redirect back to the homepage.
#     if username != None: 
#         return render_template("top-melons.html", 
#                         loved_melons=melons,
#                         name=username)
#     else:
#         return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    
    # Set to false for smooth redirect to top-melons??
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
