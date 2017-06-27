from flask import Flask, request, jsonify, abort
import database_helper
import spotipy_util
import util
import threading
from copy import deepcopy

# initialization phase: load everything in memory

# load poi_artists_path
poi_artists = database_helper.load_poi_artists()

# load pois
pois = database_helper.load_pois(poi_artists)
print(len(pois))
print(pois)

# load playlists
playlist_collection = database_helper.PlaylistCollection(pois, poi_artists)
print(playlist_collection.playlist_dict)

# load tracks
tracks_collection = database_helper.load_tracks()

# create application
app = Flask(__name__)

# define endpoints


@app.route('/')
def home_page():
    return 'hello world'


@app.route('/position')
def position():
    # /position?lat=43.697093&lon=7.270747
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
def get_playlist_name():
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
    print(near_pois)
    playlist_name = util.create_playlist_name(near_pois)
    print(playlist_name)

    if playlist_collection.get_playlist(playlist_name) is None:
        # playlist is not in the collection
        playlist = spotipy_util.create_playlist(playlist_name)

        # select tracks
        tracks_path = util.select_tracks(playlist_name, pois, poi_artists)

        # add tracks
        print(tracks_path)
        tracks = [_[0] for _ in tracks_path]
        print(playlist['id'])
        print(tracks)
        spotipy_util.add_tracks(playlist['id'], tracks)

        playlist_object = dict()
        playlist_object['name'] = playlist_name
        playlist_object['id'] = playlist['id']
        playlist_object['tracks_paths'] = tracks_path
        playlist_collection.put_playlist(playlist_name,playlist_object)
        # get the correct playlist from the playlist collection
        res = playlist_collection.get_playlist(playlist_name)
        # reshape playlist
        res['tracks_paths'] = {x[0]:{"path":x[1],"label": tracks_collection[x[0]]} for x in res['tracks_paths']}
        print(res)
        return jsonify(res)
    else:
        # get the correct playlist from the playlist collection
        res = playlist_collection.get_playlist(playlist_name)
        # reshape playlist
        res['tracks_paths'] = {x[0]:{"path":x[1],"label": tracks_collection[x[0]]} for x in res['tracks_paths']}
        print(res)
        return jsonify(res)

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
