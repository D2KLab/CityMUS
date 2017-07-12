
# coding: utf-8

# In[14]:

import csv
import os
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper,TURTLE,JSON
from pandas_ml import ConfusionMatrix
import pandas as pd
from sklearn import metrics
from pprint import pprint
import csv
import os
import json
import spotipy

from SPARQLWrapper import SPARQLWrapper,TURTLE,JSON
from pandas_ml import ConfusionMatrix
import pandas as pd
from sklearn import metrics

from spotipy.oauth2 import SpotifyClientCredentials
clientid = '2b4bba8dba4d406a8086f33b644ddcd0'
clientsecret = 'dc13827b3900467383a12e803b10e52f'
redirect = 'http://localhost'
username = 'fabio_ellena'


# In[34]:

def get_artist_tracks(artist_name):
    client_credentials_manager = SpotifyClientCredentials(client_id=clientid,client_secret=clientsecret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False

    # get matching artist

    results = sp.search(q='artist:' + artist_name, type='artist')
    artists = results['artists']['items']
    artist = None
    if len(artists) == 0:
        return None
    
    #take most popular
    # here we can also filter by genre
    artist = max(artists, key=lambda x: x['popularity'])

    top_tracks = sp.artist_top_tracks(artist['id'], country='FR')['tracks']
    if len(top_tracks) < 10:
        return None
    return_tracks = []
    for track in top_tracks:
        return_tracks.append((track['id'], track['name']))
    return return_tracks

def get_dbpedia_label(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
                        SELECT ?label ?preferredLabel 
            WHERE { 
               <%s> rdfs:label ?label .
            FILTER (lang(?label) = "" || lang(?label) = "en") 
               OPTIONAL { 
                 <%s> rdfs:label ?preferredLabel . 
                 FILTER (lang(?preferredLabel) = "" || lang(?preferredLabel) = "en") 
               } 
            } limit 1
                        """ % (uri, uri))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    label = None
    for artist in results['results']['bindings']:
        try:
            label = artist['preferredLabel']['value']
        except KeyError:
            label = artist['label']['value']
        return label

def get_doremus_label(uri):
    sparql = SPARQLWrapper("http://data.doremus.org/sparql")
    sparql.setQuery("""
                        SELECT ?label 
            WHERE { 
               <%s> foaf:name ?label .
            } limit 1
                        """ % (uri))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    label = None
    for artist in results['results']['bindings']:
            label = artist['label']['value']
    return label


# In[29]:

POIS_PATH = os.path.normpath('doremus_dbpedia_artists.csv')

with open(POIS_PATH, 'r') as input_fp:

    reader = csv.reader(input_fp, )
    # skip header
    reader.next()
    artists = dict()
    count = 0
    for row in reader:
        count +=1
        if count % 10 == 0:
            print(count)
        artist = dict()
        artist['doremus_uri'] = row[0]
        artist['dbpedia_uri'] = row[1]
        artist['score'] = float(row[2])
        if match['score'] > 0.7:
            continue
        artist['doremus_label'] = get_doremus_label(artist['doremus_uri'])
        artist['dbpedia_label'] = get_dbpedia_label(artist['dbpedia_uri'])
        if artist['doremus_label'] is not None:
            artist['tracks'] = get_artist_tracks(artist['doremus_label'])
            if artist['tracks'] is not None:
                artists[artist['dbpedia_uri']] = artist


# In[43]:

with open('artists_tracks.json', 'wb') as out_fp:
    json.dump(artists,out_fp)


# In[42]:

for artist in artists:
    print(len(artists[artist]['tracks']))

