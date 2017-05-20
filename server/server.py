from flask import Flask, request, jsonify
import json
import database_helper
import spotipy.create_playlist_add_tracks as spot



from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work

#client = MongoClient('localhost', 27017)    #Configure the connection to the database
#db = client.camp2016    #Select the database
#todos = db.todo #Select the collection


#initialization phase: load everything in memory

pois = database_helper.load_pois()


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
        return jsonify({'Lat': lat, 'Lon': lon, 'correct': 'no'})
        # abort(404)
    if lat < -90 or lat > +90:
        return jsonify({'Lat': lat, 'Lon': lon, 'correct': 'no'})
    if lon < -180 or lon > +180:
        return jsonify({'Lat': lat, 'Lon': lon, 'correct': 'no'})

    # latitude and longitude are correct

    return jsonify({'Lat': lat, 'Lon': lon, 'correct': 'yes'})


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
