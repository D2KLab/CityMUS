from flask import Flask, request, jsonify, abort
import json
import database_helper
import spotipy_util
import util
import threading




from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work

#client = MongoClient('localhost', 27017)    #Configure the connection to the database
#db = client.camp2016    #Select the database
#todos = db.todo #Select the collection


#initialization phase: load everything in memory

pois = database_helper.load_pois()
playlist_lock = threading.Lock()
playlist_dict = spotipy_util.get_playlists_dict()
print(playlist_dict)
track_ids = ["1pAyyxlkPuGnENdj4g7Y4f", "7D2xaUXQ4DGY5JJAdM5mGP"]

app = Flask(__name__)


@app.route('/')
def home_page():
    return 'hello world'

# Here starts the serious stuff


@app.route('/position')
def position():
    # show the coordinates
    lat = request.args.get('lat', default=None, type=float)
    lon = request.args.get('lon', default=None, type=float)
    if lat is None or lon is None:
        abort(404)
        # abort(404)
    if lat < -90 or lat > +90:
        abort(404)
    if lon < -180 or lon > +180:
        abort(404)


    # latitude and longitude are correct
    # find nearest poi
    point = (lat, lon)
    near_pois = util.get_near_pois(point, pois)

    return jsonify(near_pois)

@app.route('/playlist_name')
def playlist_name():
    # show the coordinates
    lat = request.args.get('lat', default=None, type=float)
    lon = request.args.get('lon', default=None, type=float)
    if lat is None or lon is None:
        abort(404)
        # abort(404)
    if lat < -90 or lat > +90:
        abort(404)
    if lon < -180 or lon > +180:
        abort(404)

    # latitude and longitude are correct
    # find nearest poi
    point = (lat, lon)
    near_pois = util.get_near_pois(point, pois)
    name = util.create_playlist_name(near_pois)
    return jsonify(name)

@app.route('/create_playlist')
def create_playlist_from_position():
    # show the coordinates
    lat = request.args.get('lat', default=None, type=float)
    lon = request.args.get('lon', default=None, type=float)
    if lat is None or lon is None:
        abort(404)
        # abort(404)
    if lat < -90 or lat > +90:
        abort(404)
    if lon < -180 or lon > +180:
        abort(404)

    # latitude and longitude are correct
    # find nearest poi
    point = (lat, lon)
    near_pois = util.get_near_pois(point, pois)
    playlist_name = util.create_playlist_name(near_pois)
    with playlist_lock:
        if playlist_name not in playlist_dict:
            playlist = spotipy_util.create_playlist(playlist_name)
            #todo: add tracks
            playlist_dict[playlist_name] = playlist['id']
            return playlist_dict[playlist_name]
        else:
            return playlist_dict[playlist_name]

@app.route('/pois')
def get_pois():
    return jsonify(pois)

# with app.test_request_context():
#     print url_for('show_coordinates', lat=123, lon=24)
#     print url_for('hello_world')
#     print url_for('show_user_profile', username='gianni')
#     print url_for('show_post', post_id=123)

if __name__ == '__main__':
    app.run()
