import csv
import os


POIS_PATH = os.path.normpath('data/dbpedia_match_nogeo_distinct.csv')


def load_pois():
    with open(POIS_PATH, 'r') as input_fp:
        reader = csv.reader(input_fp, )
        # skip header
        reader.next()
        pois = []
        for row in reader:
            poi = dict()
            poi['label'] = row[2]
            poi['uri'] = row[3]
            poi['lat'] = row[5]
            poi['long'] = row[6]
            pois.append(poi)
        return pois
