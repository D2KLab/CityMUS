import csv
import json
import os
from threading import Lock
import spotipy_util
from copy import deepcopy


POIS_PATH = os.path.normpath('data/dbpedia_match_nogeo_distinct.csv')
POIS_ARTISTS_PATH = os.path.normpath('data/poi_artist_path.json')
TRACKS_ARTISTS_PATH = os.path.normpath('data/tracks.json')


def load_pois(poi_artists):
    with open(POIS_PATH, 'r') as input_fp:
        count = 1
        reader = csv.reader(input_fp, )
        # skip header
        reader.next()
        pois = []
        for row in reader:
            poi = dict()
            poi['id'] = count
            poi['label'] = row[2]
            poi['uri'] = row[3]
            poi['latitude'] = float(row[5])
            poi['longitude'] = float(row[6])
            if poi['uri'] in poi_artists:
                pois.append(poi)
                count += 1
        return pois


def load_poi_artists():
    with open(POIS_ARTISTS_PATH, 'r') as input_fp:
        poi_artists = json.load(input_fp)
        return poi_artists

def load_tracks():
    with open(TRACKS_ARTISTS_PATH, 'r') as input_fp:
        tracks = json.load(input_fp)
        return tracks




class PlaylistCollection:
    def __init__(self, pois, poi_artists):
        self.lock = Lock()
        self.playlist_dict = spotipy_util.get_playlists_dict(pois, poi_artists)

    def get_playlist(self, playlist_name):
        with self.lock:
            if playlist_name not in self.playlist_dict:
                return None
            else:
                return deepcopy(self.playlist_dict[playlist_name])

    def put_playlist(self, playlist_name, playlist):
        with self.lock:
            new_playlist = deepcopy(playlist)
            self.playlist_dict[playlist_name] = new_playlist

