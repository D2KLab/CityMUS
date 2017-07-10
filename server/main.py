from flask import Flask, request, jsonify, abort, make_response, current_app
import database_helper
import spotipy_util
import util
import threading
from datetime import timedelta
from functools import update_wrapper
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

# Cross-domain Decorator
# https://stackoverflow.com/a/22182389/1218213
# or http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
  """Decorator function that allows crossdomain requests.
    Courtesy of
    https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
  """
  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
    headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
    origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    """ Determines which methods are allowed
    """
    if methods is not None:
      return methods

    options_resp = current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f):
    """The decorator function
    """
    def wrapped_function(*args, **kwargs):
      """Caries out the actual cross domain code
      """
      if automatic_options and request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()
      else:
        resp = make_response(f(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
        return resp

      h = resp.headers
      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      h['Access-Control-Allow-Credentials'] = 'true'
      h['Access-Control-Allow-Headers'] = \
          "Origin, X-Requested-With, Content-Type, Accept, Authorization"
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

    f.provide_automatic_options = False
    return update_wrapper(wrapped_function, f)
  return decorator

# define endpoints


@app.route('/')
@crossdomain(origin='*')
def home_page():
    return 'hello world'


@app.route('/position')
@crossdomain(origin='*')
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
@crossdomain(origin='*')
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
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def get_pois():
    return jsonify(pois)

# with app.test_request_context():
#     print url_for('show_coordinates', lat=123, lon=24)
#     print url_for('hello_world')
#     print url_for('show_user_profile', username='gianni')
#     print url_for('show_post', post_id=123)

if __name__ == '__main__':
    app.run()
