import csv
from pprint import pprint
import json
import os


POIS_PATH = os.path.normpath('../data/dbpedia_match_nogeo_distinct.csv')


def get_linked_artists():
    with open('../data/artists_tracks.json', 'r') as input_fp:
        artists = json.load(input_fp)

        artists = artists.keys()


with open(POIS_PATH, 'r') as input_fp:
    count = 0
    reader = csv.reader(input_fp, )
    # skip header
    reader.next()

    links = dict()
    for row in reader:
        poi_uri = row[3]
        link_artist = get_linked_artists()
        links[poi_uri] = link_artist

with open('../data/poi_artists.json', 'wb') as output_fp:
    json.dump(links, output_fp)
