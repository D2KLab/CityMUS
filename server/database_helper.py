import csv
import json
import os


POIS_PATH = os.path.normpath('data/dbpedia_match_nogeo_distinct.csv')
ARTISTS_PATH = os.path.normpath('data/dbpedia_match_artists.csv')


def load_pois():
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
            poi['lat'] = float(row[5])
            poi['long'] = float(row[6])
            pois.append(poi)
            count += 1
        return pois

def load_artists_tracks():
    with open(ARTISTS_PATH, 'r') as input_fp:
        reader = csv.reader(input_fp, )
        # skip header
        reader.next()
        artists = dict()
        for row in reader:
            artist = dict()
            artist['doremus_uri'] = None
            artist['doremus_label'] = row[2]
            artist['dbpedia_uri'] = row[3]
            artist['dbpedia_label'] = row[3]
            artist['spotify_uri'] = row[3]
            artist['tracks'] = None
            artists[artist['doremus_uri']] = artist

        return artists