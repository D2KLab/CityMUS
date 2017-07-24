from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id='4b115cf521ba4691a64a622eb3158f44', client_secret='8d8e24a769cf4f6797e6325b33b16016')

import csv
import os
import json
import spotipy
import pickle


from SPARQLWrapper import SPARQLWrapper, JSON


def get_artist_tracks(artist_name):
    
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False

    # get matching artist

    results = sp.search(q='artist:' + artist_name, type='artist')
    artists = results['artists']['items']
    artist = None
    if len(artists) == 0:
        return None
    artist = max(artists, key=lambda x: x['popularity'])

    top_tracks = sp.artist_top_tracks(artist['id'], country='FR')['tracks']
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
                 FILTER (lang(?preferredLabel) = "" || lang(?preferredLabel) = "tk") 
               } 
            } limit 1
                        """ % (uri, uri))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

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


ARTIST_PATH = os.path.normpath('../data/doremus_dbpedia_artists.csv')

trace = 0
with open(ARTIST_PATH, 'r') as input_fp:
    trace += 1
    count = 0
    reader = csv.reader(input_fp, )
    # skip header
    reader.next()
    artists = dict()
    rows = []
    for row in reader:
        artist = dict()
        artist['doremus_uri'] = row[0]
        artist['doremus_label'] = get_doremus_label(artist['doremus_uri'])
        artist['dbpedia_uri'] = row[1]
        artist['dbpedia_label'] = get_dbpedia_label(artist['dbpedia_uri'])
        artist['tracks'] = get_artist_tracks(artist['doremus_label'])
        if artist['tracks'] is not None:
            count += 1
            print(count)
            artists[artist['doremus_uri']] = artist
        if trace % 100 == 0:
            pickle.dump( artist, open( "artist.p", "wb" ) )
            pickle.dump( trace, open( "trace.p", "wb" ) )
            

ARTIST_PATH = os.path.normpath('../data/artists_tracks.json')

with open(ARTIST_PATH, 'wb') as output_fp:
    json.dump(artists, output_fp)
print(len(artists))
