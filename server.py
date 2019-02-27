# For feeding variables to templates.
from jinja2 import StrictUndefined

# For helpful debugging.
from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# Tables for jQuery.
from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 
# For API calls.
from sqlalchemy import cast, Numeric
import requests
# For Chartjs color generation.
import random

# Create Flask app.
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required for Flask sessions and debug toolbar use
app.secret_key = "ABC"

@app.route("/")
def index():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/search_result", methods=['GET'])
def return_search_result():
    """Return user's search results."""

    # Search string user enters gathered from the form on the homepage.
    search_str = request.args.get("search_str")

    # Return the producer(s), performer(s), song(s), and album(s)
    # that match the search string (not case-sensitive), alphabetized.
    if len(search_str) > 0:
        producers = Producer.query.order_by('producer_name').filter(Producer.producer_name.ilike('%{}%'.format(search_str))).all()
        performers = Performer.query.order_by('performer_name').filter(Performer.performer_name.ilike('%{}%'.format(search_str))).all()
        songs = Song.query.order_by('song_title').filter(Song.song_title.ilike('%{}%'.format(search_str))).options(db.joinedload("performers")).all()
        albums = Album.query.order_by('album_title').filter(Album.album_title.ilike('%{}%'.format(search_str))).options(db.joinedload("performers")).all()
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

    # Query for all producers in database; return results alphabetized.
    producers = Producer.query.order_by('producer_name').all()

    return render_template("producer_list.html", producers=producers)


# Each producer's page's url will include the producer's database id.
@app.route("/producers/<int:producer_id>")
def producer_detail(producer_id):
    """Show producer's details."""

    # URL from which to make API calls.
    URL = "https://genius.com/api/artists/" + str(producer_id)

    # Method "joinedload" employed to reduce # of queries run for output.
    producer = Producer.query.options(db.joinedload("albums")
                                        .joinedload("songs")
                                        .joinedload("producers")
                                      ).get(producer_id)

    albums = producer.albums # list
    # Return the album release years in descending chronological order.
    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    r = requests.get(URL)
    j = r.json()
    
    # If call is successful, access JSON object.
    if j['meta']['status'] == 200:
        bio = j['response']['artist'].get('description_preview',"")

    # Store producer_id in session.
    session["producer_id"] = producer_id

    return render_template("producer.html",
                            producer=producer,
                            album_years=album_years,
                            bio=bio
                          )


@app.route('/producer-frequency.json')
def generate_producer_performer_frequency_donut_chart():
    """Create producer to performer frequency donut chart."""

    # Retrieve producer_id from the session for producer_song_tuples query.
    producer_id = session["producer_id"]

    # Create list of tuples; value @ 1st index = performer_name; 
    # value @ 2nd = song count.
    producer_song_tuples = db.session.query(Performer.performer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id).group_by(
                            Performer.performer_name).order_by(Performer.performer_name).all()

    # Python dictionary to jsonfiy and pass to front end to build chartjs viz.
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
    }

    # Loop through range of song tuple to feed labels (performer_name) 
    # and data (song counts) to dictionary.
    for i in range(0, len(producer_song_tuples)):
        performer = producer_song_tuples[i][0]
        data_dict["labels"].append(performer)
        i+=1

    for j in range(0, len(producer_song_tuples)):
        song_count = producer_song_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # Generate chart colors using random's randint method.
    for k in range(0, len(producer_song_tuples)):
        random_red = random.randint(0,255)
        random_green = random.randint(0,255)
        random_blue = random.randint(0,255)
        random_color = "rgba(" + str(random_red) + "," + str(random_green) + "," + str(random_blue) + ",1)"
        data_dict["datasets"][0]["backgroundColor"].append(random_color)
        k+=1

    return jsonify(data_dict)


# @app.route('/producer-bubbles.json')
# def generate_producer_bubbles():
#     """Create bubbles on producer page of performer frequencies."""

#     # Retrieve producer_id from the session for producer_song_tuples query.          
#     producer_id = session["producer_id"]

#     # Create list of tuples.
#     producer_song_tuples = db.session.query(Performer.performer_name,Performer.performer_id,
#                             db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
#                             ProduceSong.producer_id==producer_id).group_by(
#                             Performer.performer_name, Performer.performer_id).all()

#     # Python dictionary to jsonfiy and pass to front end to build chartjs viz.
#     bubl_dict = {
#                 "name": "performers",
#                 "value": 100,
#                 "children": []
#             }

#     for i in range(0, len(producer_song_tuples)):
#         bubl_pre_dic = {}
#         bubl_pre_dic["domain"] = producer_song_tuples[i][0]
#         bubl_pre_dic["name"] = producer_song_tuples[i][0]
#         bubl_pre_dic["link"] = producer_song_tuples[i][1]
#         bubl_pre_dic["value"] = producer_song_tuples[i][2]
#         bubl_dict["children"].append(bubl_pre_dic)
#         i+=1

#     return jsonify(bubl_dict)


@app.route('/producer-productivity.json')
def producer_productivity_data():
    """Return producer productivity JSON for line Chartjs data viz."""
    
    # Get producer_id from id stored in session.
    producer_id = session["producer_id"]

    # Return tuples of song_release_year and song counts for every producer from 
    # the years 1900 - 2019.  Correcting for year data pulled from Genius API 
    # that may be an incorrect year.
    producer_song_tuples = db.session.query(Song.song_release_year,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id 
                            , Song.song_release_year != None
                            , cast(Song.song_release_year, Numeric(10, 4)) > 1900
                            , cast(Song.song_release_year, Numeric(10, 4)) < 2019).group_by(Song.song_release_year).order_by(Song.song_release_year).all()

    data_dict = {
        "labels": [],
        "datasets": [
            {
                "label": "Number of Songs Produced",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(0,255,0,0.1)",
                "borderColor": "rgba(220,220,220,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(220,220,220,1)",
                "pointBackgroundColor": "green",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "green",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": [],
                "spanGaps": False
            }
        ]
    }

    # Loop through producer song tuples, making the value of the 1st index in
    # the tuple (year) the labels and the 2nd index value (song counts) the data
    for i in range(0, len(producer_song_tuples)):
        data_dict["labels"].append(producer_song_tuples[i][0])
        data_dict["datasets"][0]["data"].append(producer_song_tuples[i][1])

    return jsonify(data_dict)


@app.route("/performers")
def performer_list():
    """Show list of performers."""

    # Return producers in database; return results alphabetized.
    performers = Performer.query.order_by('performer_name').all()

    return render_template("performer_list.html", performers=performers)


# Each performer's page's url will include the performer's database id.
@app.route("/performers/<int:performer_id>", methods=["GET"])
def performer_detail(performer_id):
    """Show performer's detail."""

    URL = "https://genius.com/api/artists/" + str(performer_id)

    performer = Performer.query.options(db.joinedload("albums")
                                          .joinedload("songs")
                                          .joinedload("performers")
                                      ).get(performer_id)
    albums = performer.albums

    # Return a set of performer's album release years in descending order.
    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    # Store performer_id in session.
    session["performer_id"] = performer_id

    # API call for producer bio.
    r = requests.get(URL)
    j = r.json()
    
    # If url request is successful and the bio JSON key exists, return that key
    # value (description_preview); otherwise, return an empty string.
    if j['meta']['status'] == 200:
        bio = j['response']['artist'].get('description_preview',"")

    return render_template("performer.html",
                            performer=performer,
                            album_years=album_years,
                            bio=bio
                          )


@app.route('/performer-frequency.json')
def generate_performer_producer_frequency_donut_chart():
    """Create JSON of performer to producer frequency."""

    # Retrieve performer_id from session.
    performer_id = session["performer_id"]

    # Return tuples of producer_names and song_counts for performer.
    performer_producer_tuples = db.session.query(Producer.producer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.performer_id==performer_id).group_by(
                            Producer.producer_name).all()

    # Dictionary Chartjs will use to create donut chart.
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # Loop through range of song_count tuple to feed data to chart, setting 
    # labels as the producer name and the song counts for each producer as the 
    # data.
    for i in range(0, len(performer_producer_tuples)):
        performer = performer_producer_tuples[i][0]
        data_dict["labels"].append(performer)
        i+=1

    for j in range(0, len(performer_producer_tuples)):
        song_count = performer_producer_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # Generate random colors for donut chart using random's randint method.
    for k in range(0, len(performer_producer_tuples)):
        random_red = random.randint(0,255)
        random_green = random.randint(0,255)
        random_blue = random.randint(0,255)
        random_color = "rgba(" + str(random_red) + "," + str(random_green) + "," + str(random_blue) + ",1)"
        data_dict["datasets"][0]["backgroundColor"].append(random_color)
        k+=1

    return jsonify(data_dict)


@app.route("/songs")
def song_list():
    """Show list of songs."""

    # SQLALchemy query to return all song titles.
    songs = Song.query.order_by("song_title").all()

    return render_template("song_list.html", 
                            songs=songs
                          )


# Each song's page's URL will include the song's database id.
@app.route("/songs/<int:song_id>", methods=["GET"])
def song_detail(song_id):
    """Show song detail."""

    # Return song objects using producers' and songs' relationship.
    song = Song.query.options(db.joinedload("producers")
                                .joinedload("songs")
                               ).get(song_id)

    return render_template("song.html",
                            song=song
                           )


@app.route("/albums")
def album_list():
    """Show list of albums."""

    # Return album objects using performers' and albums' relationship, ordering
    # results by album title.
    albums = Album.query.options(db.joinedload("performers")
                                   .joinedload("albums")
                                  ).order_by('album_title').all()

    return render_template("album_list.html", 
                            albums=albums
                          )


# each album's page's url will include the album's database id
@app.route("/albums/<int:album_id>", methods=["GET"])
def album_detail(album_id):
    """Show album details."""

    # url from which to make API calls
    URL = "https://genius.com/api/albums/" + str(album_id)

    # SQLAlchemy query to return album objects using album_id argument using 
    # songs' and albums' relationship.
    album = Album.query.options(db.joinedload("songs")
                                  .joinedload("albums")
                                 ).get(album_id)

    # Storing album_id in session.
    session["album_id"] = album_id

    # API call to return album bio.
    r = requests.get(URL)
    j = r.json()
    
    # If call is successful, return 'description_preview' value in JSON object.
    if j["meta"]["status"] == 200:
        bio = j["response"]["album"].get("description_preview","")
    
    return render_template("album.html",
                            album=album,
                            bio=bio
                          )


@app.route("/album-bubbles.json")
def generate_album_bubbles():
    """Create producer to album frequency bubble Chartjs vis."""

    # Retrieve producer_id from the session for album_producer_tuples query.          
    album_id = session["album_id"]

    # SQLAlchemy query creates list of tuples of producer's name, image url, and
    # count of songs.
    album_producer_tuples = db.session.query(Producer.producer_name, Producer.producer_img_url,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.album_id==album_id).group_by(
                            Producer.producer_name, Producer.producer_img_url).all()

    # Python dictionary to jsonfiy and pass to front end to build chartjs viz.
    bubl_dict = {
                "name": "producers",
                "value": 100,
                "children": []
            }

    # Loop through album_producer_tuples to create dictionaries for every
    # producer and append them to dictionary that will be used to create D3
    # pack-force graph.
    for i in range(0, len(album_producer_tuples)):
        bubl_pre_dic = {}
        bubl_pre_dic["domain"] = album_producer_tuples[i][0]
        bubl_pre_dic["name"] = album_producer_tuples[i][0]
        bubl_pre_dic["link"] = album_producer_tuples[i][1]
        bubl_pre_dic["value"] = album_producer_tuples[i][2]
        bubl_dict["children"].append(bubl_pre_dic)
        i+=1

    return jsonify(bubl_dict)


@app.route("/album-web.json")
def generate_album_web():
    """Create album web D3 viz."""

    # Retrieve producer_id from the session for album_producer_tuples query.
    album_id = session["album_id"]

    # SQLAlchemy query creates tuples of album cover art url for dictionary used 
    # to create D3 viz.
    album_img = db.session.query(Album.cover_art_url).filter(Album.album_id==album_id).one()

    # SQLAlchemy query creates tupes of producer's name, image, the cover art of
    # the album they produced and the songs on that album they produced.
    album_producer_tuples = db.session.query(Producer.producer_name, Producer.producer_img_url,Album.cover_art_url,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).join(Album).filter(
                            ProduceSong.album_id==album_id, Album.album_id==ProduceSong.album_id).group_by(
                            Producer.producer_name, Producer.producer_img_url, Album.cover_art_url).all()

    # JSON object that will be jsonified and used to create D3 viz.
    album_dict = {
         "name": album_id,
         "img": album_img[0],
         "children": [
              {
               "name": "Producers",
               "children": []
              }
          ]
    }

    # Loop through range for album_producer_tuples, updating album_dict with the
    # necessary values from tuples generate w/SQLAlchemy query above.
    for i in range(0, len(album_producer_tuples)):
        child_dic = {}
        if album_producer_tuples[i][3] > 1:
            child_dic["hero"] = str(album_producer_tuples[i][0]) +  " (" + str(album_producer_tuples[i][3]) + " songs)" 
            child_dic["name"] = str(album_producer_tuples[i][0]) + " (" + str(album_producer_tuples[i][3]) + " songs)" 
        else: 
            child_dic["hero"] = str(album_producer_tuples[i][0]) +  " (" + str(album_producer_tuples[i][3]) + " song)" 
            child_dic["name"] = str(album_producer_tuples[i][0]) + " (" + str(album_producer_tuples[i][3]) + " song)" 
        child_dic["link"] = album_producer_tuples[i][1]
        child_dic["img"] = album_producer_tuples[i][1]
        child_dic["size"] = 40000
        album_dict["children"][0]["children"].append(child_dic)
        i+=1

    return jsonify(album_dict)


@app.route('/album-frequency.json')
def generate_album_producer_frequency_donut_chart():
    """Create album producer frequency donut chart."""

    # Set value of album_id to the album_id value stored in session.
    album_id = session["album_id"]

    # Retrun tuples of producer's name and the count of songs they have created
    # on the album queries.
    album_producer_tuples = db.session.query(Producer.producer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.album_id==album_id).group_by(
                            Producer.producer_name).all()

    # Used to build data dictionary Chartjs will use to create data viz.
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # Loop through range of tuples to feed data to chart.
    for i in range(0, len(album_producer_tuples)):
        producers = album_producer_tuples[i][0]
        data_dict["labels"].append(producers)
        i+=1

    for j in range(0, len(album_producer_tuples)):
        song_count = album_producer_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # Generate chart's colors with random library's "randint" method.
    for k in range(0, len(album_producer_tuples)):
        random_red = random.randint(0,255)
        random_green = random.randint(0,255)
        random_blue = random.randint(0,255)
        random_color = "rgba(" + str(random_red) + "," + str(random_green) + "," + str(random_blue) + ",1)"
        data_dict["datasets"][0]["backgroundColor"].append(random_color)
        k+=1

    return jsonify(data_dict)


def make_nodes_and_paths(filename):
    """Make nodes and paths for music industry D3 chart."""

    # File = export of sql query entered at command line: 
    # psql -d music -t -A -F"," -c "select performer_name, 
    # producer_name from produce_song ps join performers p using (performer_id) 
    # oin producers using (producer_id)" > output.csv.
    file_obj = open(filename)
    contents = file_obj.read()
    lines = contents.split('\n') # Create a list of the rows in the file.

    nodes = {} # Focal point of data (words).
    for pair in lines:
        split = pair.split(',') # split each line, using a comma as a delimitor
        if split: # If pair is not blank (line in file was not blank),
            # for loop through split list, bind each item to variable node.
            for node in split: 
                node = node.strip() # Strip each pair in list of white space.
                if not nodes.get(node):
                    nodes[node] = split[1].strip()
    
    nodes = [{'name':node, 'parent': nodes[node]} for node in nodes.keys()]

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['parent'])

    paths = []
    for line in lines:
        slt = line.split(',') # Split line in csv by comma.
        if len(slt) == 2:
            source, target = slt
            paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]  })

    return nodes, paths


@app.route("/data.json")
def get_graph_data():
    """JSON read to create music industry D3 Chart."""

    # Call helper functions.
    # Read filename fed in as argument.
    nodes, paths = make_nodes_and_paths('output3.csv')
    # Create a json object of the list of nodes and list of paths.
    return jsonify({'nodes':nodes, 'paths':paths}) 



@app.route("/network")
def graph():
    """Show music industry D3 Chart."""

    return render_template("network.html")


@app.route('/resume')
def resume():
    """Show resume."""

    return render_template("resume.html")


################################################################################

if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")















