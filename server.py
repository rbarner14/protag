# for feeding variables to templates
from jinja2 import StrictUndefined

# for helpful debugging
from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

#tables for jquery
from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 

# create Flask app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required for Flask sessions and debug toolbar use
app.secret_key = "ABC"

# def make_nodes_and_paths(filename):
#     file_obj = open(filename)
#     contents = file_obj.read()
#     lines = contents.split('\n')
#     print(lines)

#     nodes = {}
#     for pair in lines:
#         split = pair.split(',')
#         if split:
#             for node in split:
#                 node = node.strip()
#                 if not nodes.get(node):
#                     nodes[node] = split[1].strip()
    
#     nodes = [{'name':node, 'parent': nodes[node]} for node in nodes.keys()]

#     index_nodes = {}
#     for idx, n in enumerate(nodes):
#         index_nodes[n['name']] = (idx, n['parent'])

#     paths = []
#     for line in lines:
#         slt = line.split(',')
#         if len(slt) == 2:
#             source, target = slt
#             paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]  })

#     return nodes, paths


def make_nodes_and_paths(filename):
    file_obj = open(filename)
    contents = file_obj.read()
    lines = contents.split('\n') # creates a list of the rows in the file
    print(lines)

    nodes = {} # focal point of data (words)
    for pair in lines:
        split = pair.split(',') # split each line, using a comma as a delimitor
        if split: # if pair is not blank (line in file was not blank)
            for node in split: # for loop through split list, each item bound to variable node
                node = node.strip() #strip each pair in list of white space
                if not nodes.get(node):
                    nodes[node] = split[1].strip()
    
    nodes = [{'name':node, 'parent': nodes[node]} for node in nodes.keys()]

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['parent'])

    paths = []
    for line in lines:
        slt = line.split(',') # split line in csv by comma
        if len(slt) == 2:
            source, target = slt
            paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]  })

    return nodes, paths


@app.route("/")
def index():

        return render_template("homepage.html")


@app.route("/data.json")
def get_graph_data():
    # call helper functions
    # read filename fed in as argument
    nodes, paths = make_nodes_and_paths('ideas.csv')
    # create a json object of the list of nodes and list of paths 
    return jsonify({'nodes':nodes, 'paths':paths}) 


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
@app.route("/producers/<int:producer_id>")
def producer_detail(producer_id):

    # joinedload reduces # of queries run for output
    producer = Producer.query.options(db.joinedload("albums")
                                        .joinedload("songs")
                                        .joinedload("producers")
                                      ).get(producer_id)

    albums = producer.albums # list
    # returns the album release years in descending chronological order
    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    session["producer_id"] = producer_id

    return render_template("producer.html",
                            producer=producer,
                            album_years=album_years
                          )


@app.route('/producer-frequency.json')
def generate_producer_performer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
                         "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
                         "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
                         "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
                         "#A0522D"]

    producer_id = session["producer_id"]

    producer_song_tuples = db.session.query(Performer.performer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id).group_by(
                            Performer.performer_name).all()

    # to build chart
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # loop through range of song_count tuple to feed data to chart
    for i in range(0, len(producer_song_tuples)):
        performer = producer_song_tuples[i][0]
        data_dict["labels"].append(performer)
        i+=1

    for j in range(0, len(producer_song_tuples)):
        song_count = producer_song_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # loop through background color list
    for k in range(0, len(background_colors)):
        bgcolor = background_colors[k]
        data_dict["datasets"][0]["backgroundColor"].append(bgcolor)
        k+=1

    return jsonify(data_dict)


@app.route("/performers")
def performer_list():
    """Show list of performers."""

    # query for all producers in database; return results alphabetized    
    performers = Performer.query.order_by('performer_name').all()

    return render_template("performer_list.html", performers=performers)


# each performer's page's url will include the performer's database id
@app.route("/performers/<int:performer_id>", methods=["GET"])
def performer_detail(performer_id):

    performer = Performer.query.options(db.joinedload("albums")
                                          .joinedload("songs")
                                          .joinedload("producers")
                                      ).get(performer_id)
    albums = performer.albums

    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    session["performer_id"] = performer_id

    return render_template("performer.html",
                            performer=performer,
                            album_years=album_years
                          )


@app.route('/performer-frequency.json')
def generate_performer_producer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
                         "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
                         "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
                         "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
                         "#A0522D"]

    performer_id = session["performer_id"]

    performer_producer_tuples = db.session.query(Producer.producer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.performer_id==performer_id).group_by(
                            Producer.producer_name).all()

    # to build chart
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # loop through range of song_count tuple to feed data to chart
    for i in range(0, len(performer_producer_tuples)):
        performer = performer_producer_tuples[i][0]
        data_dict["labels"].append(performer)
        i+=1

    for j in range(0, len(performer_producer_tuples)):
        song_count = performer_producer_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # loop through background color list
    for k in range(0, len(background_colors)):
        bgcolor = background_colors[k]
        data_dict["datasets"][0]["backgroundColor"].append(bgcolor)
        k+=1

    return jsonify(data_dict)



@app.route("/songs")
def song_list():
    """Show list of songs."""

    songs = Song.query.options(db.joinedload("performers")
                              ).order_by('song_title').all()

    return render_template("song_list.html", 
                            songs=songs
                          )


# each song's page's url will include the song's database id
@app.route("/songs/<int:song_id>", methods=["GET"])
def song_detail(song_id):

    song = Song.query.options(db.joinedload("producers")).get(song_id)

    return render_template("song.html",
                            song=song
                           )


@app.route("/albums")
def album_list():
    """Show list of albums."""

    albums = Album.query.options(db.joinedload("producers")
                                   .joinedload("songs")
                                  ).order_by('album_title').all()

    return render_template("album_list.html", 
                            albums=albums
                          )

# each album's page's url will include the album's database id
@app.route("/albums/<int:album_id>", methods=["GET"])
def album_detail(album_id):

    album = Album.query.get(album_id)

    session["album_id"] = album_id
    
    return render_template("album.html",
                            album=album
                          )


@app.route('/album-frequency.json')
def generate_album_producer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
                         "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
                         "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
                         "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
                         "#A0522D"]

    album_id = session["album_id"]

    album_producer_tuples = db.session.query(Producer.producer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.album_id==album_id).group_by(
                            Producer.producer_name).all()

    # to build chart
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # loop through range of song_count tuple to feed data to chart
    for i in range(0, len(album_producer_tuples)):
        producers = album_producer_tuples[i][0]
        data_dict["labels"].append(producers)
        i+=1

    for j in range(0, len(album_producer_tuples)):
        song_count = album_producer_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # loop through background color list
    for k in range(0, len(background_colors)):
        bgcolor = background_colors[k]
        data_dict["datasets"][0]["backgroundColor"].append(bgcolor)
        k+=1

    return jsonify(data_dict)


################################################################################

if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")















