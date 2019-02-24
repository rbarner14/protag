# for feeding variables to templates
from jinja2 import StrictUndefined

# for helpful debugging
from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# tables for jquery
from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 
# for api calls
import requests
import random

# create Flask app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required for Flask sessions and debug toolbar use
app.secret_key = "ABC"

def make_nodes_and_paths(filename):
    # file = export of sql query: 
    # psql -d music -t -A -F"," -c "select performer_name, 
    # producer_name from produce_song ps join performers p using (performer_id) 
    # join producers using (producer_id)" > output.csv
    file_obj = open(filename)
    contents = file_obj.read()
    lines = contents.split('\n') # creates a list of the rows in the file
    # print(lines)

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


@app.route("/network")
def graph():

    return render_template("network.html")

@app.route("/data.json")
def get_graph_data():
    # call helper functions
    # read filename fed in as argument
    nodes, paths = make_nodes_and_paths('output3.csv')
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

    # url from which to make API calls
    URL = "https://genius.com/api/artists/" + str(producer_id)

    # joinedload reduces # of queries run for output
    producer = Producer.query.options(db.joinedload("albums")
                                        .joinedload("songs")
                                        .joinedload("producers")
                                      ).get(producer_id)

    albums = producer.albums # list
    # returns the album release years in descending chronological order
    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    r = requests.get(URL)
    j = r.json()
    
    # if call is successful, access json object
    if j['meta']['status'] == 200:
        bio = j['response']['artist'].get('description_preview',"")

    session["producer_id"] = producer_id

    return render_template("producer.html",
                            producer=producer,
                            album_years=album_years,
                            bio=bio
                          )

@app.route('/producer-bubbles.json')
def generate_producer_bubbles():

    # retrieve producer_id from the session for producer_song_tuples query          
    producer_id = session["producer_id"]

    # query creates list of tuples
    producer_song_tuples = db.session.query(Performer.performer_name,Performer.performer_id,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id,Performer.performer_id!=producer_id).group_by(
                            Performer.performer_name, Performer.performer_id).all()

    # python dictionary to jsonfiy and pass to front end to build chartjs viz 
    bubl_dict = {
                "name": "performers",
                "value": 100,
                "children": []
            }

    for i in range(0, len(producer_song_tuples)):
        bubl_pre_dic = {}
        bubl_pre_dic["domain"] = producer_song_tuples[i][0]
        bubl_pre_dic["name"] = producer_song_tuples[i][0]
        bubl_pre_dic["link"] = producer_song_tuples[i][1]
        bubl_pre_dic["value"] = producer_song_tuples[i][2]
        bubl_dict["children"].append(bubl_pre_dic)
        i+=1

    return jsonify(bubl_dict)

@app.route('/producer-productivity.json')
def producer_productivity_data():
    """Return time series data of Melon Sales."""
    producer_id = session["producer_id"]

    producer_song_tuples = db.session.query(Song.song_release_year,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id, Song.song_release_year != None).group_by(
                            Song.song_release_year).order_by(Song.song_release_year).all()

    data_dict = {
        # "labels": ["January", "February", "March", "April", "May", "June", "July"],
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
                # "data": [65, 59, 80, 81, 56, 55, 40],
                "data": [],
                "spanGaps": False
            }
        ]
    }

    for i in range(0, len(producer_song_tuples)):
        data_dict["labels"].append(producer_song_tuples[i][0])
        data_dict["datasets"][0]["data"].append(producer_song_tuples[i][1])

    print(data_dict)
    return jsonify(data_dict)

@app.route('/producer-frequency.json')
def generate_producer_performer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    # background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
    #                      "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
    #                      "#A0522D","#00BFFF", "#808000", "#F0E68C", "#9ACD32"]

    # retrieve producer_id from the session for producer_song_tuples query          
    producer_id = session["producer_id"]

    # query creates list of tuples
    producer_song_tuples = db.session.query(Performer.performer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.producer_id==producer_id).group_by(
                            Performer.performer_name).order_by(Performer.performer_name).all()

    # python dictionary to jsonfiy and pass to front end to build chartjs viz 
    data_dict = {
                "labels": [],
                "datasets": [
                    {
                        "data": [],
                        "backgroundColor": [],
                        "hoverBackgroundColor": []
                    }]
            }

    # loop through range of song_count tuple to feed labels and data to 
    # dictionary
    for i in range(0, len(producer_song_tuples)):
        performer = producer_song_tuples[i][0]
        data_dict["labels"].append(performer)
        i+=1

    for j in range(0, len(producer_song_tuples)):
        song_count = producer_song_tuples[j][1]
        data_dict["datasets"][0]["data"].append(song_count)
        j+=1

    # loop through background color list
    for k in range(0, len(producer_song_tuples)):
        random_red = random.randint(0,255)
        random_green = random.randint(0,255)
        random_blue = random.randint(0,255)
        random_color = "rgba(" + str(random_red) + "," + str(random_green) + "," + str(random_blue) + ",1)"
        print(random_color)
        data_dict["datasets"][0]["backgroundColor"].append(random_color)
        k+=1

    # print(data_dict)
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

    URL = "https://genius.com/api/artists/" + str(performer_id)

    performer = Performer.query.options(db.joinedload("albums")
                                          .joinedload("songs")
                                          .joinedload("performers")
                                      ).get(performer_id)
    albums = performer.albums

    album_years = sorted(set([album.album_release_date.strftime("%Y") for album in albums]),reverse=True)

    session["performer_id"] = performer_id

    r = requests.get(URL)
    j = r.json()
    
    if j['meta']['status'] == 200:
        bio = j['response']['artist'].get('description_preview',"")

    return render_template("performer.html",
                            performer=performer,
                            album_years=album_years,
                            bio=bio
                          )


@app.route('/performer-frequency.json')
def generate_performer_producer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    # background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
    #                      "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
    #                      "#A0522D","#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
    #                      "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
    #                      "#A0522D","#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
    #                      "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
    #                      "#A0522D","#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6"]

    performer_id = session["performer_id"]

    performer_producer_tuples = db.session.query(Producer.producer_name,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.performer_id==performer_id, Producer.producer_id!=performer_id).group_by(
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
    # for k in range(0, len(background_colors)):
    #     bgcolor = background_colors[k]
    #     data_dict["datasets"][0]["backgroundColor"].append(bgcolor)
    #     k+=1
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
    songs = Song.query.order_by('song_title').all()
    # songs = Song.query.options(db.joinedload("performers")
    #                              .joinedload("songs")
    #                             ).order_by('song_title').all()

    return render_template("song_list.html", 
                            songs=songs
                          )


# each song's page's url will include the song's database id
@app.route("/songs/<int:song_id>", methods=["GET"])
def song_detail(song_id):

    song = Song.query.options(db.joinedload("producers")
                                .joinedload("songs")
                               ).get(song_id)

    return render_template("song.html",
                            song=song
                           )


@app.route("/albums")
def album_list():
    """Show list of albums."""

    albums = Album.query.options(db.joinedload("performers")
                                   .joinedload("albums")
                                  ).order_by('album_title').all()

    return render_template("album_list.html", 
                            albums=albums
                          )

# each album's page's url will include the album's database id
@app.route("/albums/<int:album_id>", methods=["GET"])
def album_detail(album_id):

    # url from which to make API calls
    URL = "https://genius.com/api/albums/" + str(album_id)

    album = Album.query.options(db.joinedload("songs")
                                  .joinedload("albums")
                                 ).get(album_id)

    session["album_id"] = album_id

    r = requests.get(URL)
    j = r.json()
    
    # if call is successful, access json object
    if j['meta']['status'] == 200:
        bio = j['response']['album'].get('description_preview',"")
    
    return render_template("album.html",
                            album=album,
                            bio=bio
                          )


@app.route('/album-bubbles.json')
def generate_album_bubbles():

    # retrieve producer_id from the session for producer_song_tuples query          
    album_id = session["album_id"]

    # query creates list of tuples
    album_producer_tuples = db.session.query(Producer.producer_name, Producer.producer_img_url,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).filter(
                            ProduceSong.album_id==album_id).group_by(
                            Producer.producer_name, Producer.producer_img_url).all()

    # python dictionary to jsonfiy and pass to front end to build chartjs viz 
    bubl_dict = {
                "name": "producers",
                "value": 100,
                "children": []
            }

    for i in range(0, len(album_producer_tuples)):
        bubl_pre_dic = {}
        bubl_pre_dic["domain"] = album_producer_tuples[i][0]
        bubl_pre_dic["name"] = album_producer_tuples[i][0]
        bubl_pre_dic["link"] = album_producer_tuples[i][1]
        bubl_pre_dic["value"] = album_producer_tuples[i][2]
        bubl_dict["children"].append(bubl_pre_dic)
        i+=1

    return jsonify(bubl_dict)

@app.route('/album-web.json')
def generate_album_web():

    # retrieve producer_id from the session for producer_song_tuples query          
    album_id = session["album_id"]

    # query creates list of tuples
    album_img = db.session.query(Album.cover_art_url).filter(Album.album_id==album_id).one()

    album_producer_tuples = db.session.query(Producer.producer_name, Producer.producer_img_url,Album.cover_art_url,
                            db.func.count(ProduceSong.song_id)).join(ProduceSong).join(Album).filter(
                            ProduceSong.album_id==album_id, Album.album_id==ProduceSong.album_id).group_by(
                            Producer.producer_name, Producer.producer_img_url, Album.cover_art_url).all()

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
        album_dict["children"].append(child_dic)
        i+=1

    return jsonify(album_dict)

@app.route('/album-frequency.json')
def generate_album_producer_frequency_donut_chart():

    # producer_collabs = ProduceSong.query.options(db.joinedload("performer")).where(ProduceSong.producer_id==producer_id).group_by(Performer.performer_name)
    # can pass producer_id to query with session
    # https://www.randomlists.com/random-color?qty=20
    # background_colors = ["#00BFFF", "#808000", "#F0E68C", "#9ACD32", "#FF0000", 
    #                      "#B22222", "#FF00FF", "#FF7F50", "#008080", "#191970",
    #                      "#B0E0E6", "#008000", "#8A2BE2", "#00FFFF", "#FFB6C1",
    #                      "#FFD700", "#FF1493","#32CD32", "#BC8F8F", "#E6E6FA",
    #                      "#A0522D"]

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
    # for k in range(0, len(background_colors)):
    #     bgcolor = background_colors[k]
    #     data_dict["datasets"][0]["backgroundColor"].append(bgcolor)
    #     k+=1
    for k in range(0, len(album_producer_tuples)):
        random_red = random.randint(0,255)
        random_green = random.randint(0,255)
        random_blue = random.randint(0,255)
        random_color = "rgba(" + str(random_red) + "," + str(random_green) + "," + str(random_blue) + ",1)"
        data_dict["datasets"][0]["backgroundColor"].append(random_color)
        k+=1


    return jsonify(data_dict)

@app.route('/resume')
def resume():

    return render_template("resume.html")

################################################################################

if __name__ == "__main__":
    # debug=True as it has to be True at when DebugToolbarExtension is invoked.
    
    app.debug = True

    connect_to_db(app)

    # Using the DebugToolbar.
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")















