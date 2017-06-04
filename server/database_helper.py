import csv
import json
import os


POIS_PATH = os.path.normpath('data/dbpedia_match_nogeo_distinct.csv')
POIS_ARTISTS_PATH = os.path.normpath('data/poi_artist_path.json')


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
