import csv
import os


POIS_PATH = os.path.normpath('data/dbpedia_match_nogeo_distinct_convert.csv')


def load_pois():
    with open(POIS_PATH, 'r') as input_fp:
        count = 0
        reader = csv.reader(input_fp, )
        # skip header
        reader.next()
        pois = []
        for row in reader:
            poi = dict()
            poi['id'] = count
            poi['label'] = row[2]
            poi['uri'] = row[3]
            poi['lat'] = row[5]
            poi['long'] = row[6]
            pois.append(poi)
            count += 1
        return pois
