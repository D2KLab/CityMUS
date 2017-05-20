#read all
#remove bus stations and add position to each 3cixty poi, remove dbpedia poi that are not in nice
#group by dbpedia uri

#foreach group:
#    keep entries with the highest score
#    remove entries with score < 90
#	 keep the nearest to the center

import csv
import urllib2
import json
from geopy.distance import vincenty
from SPARQLWrapper import SPARQLWrapper,JSON

NICE_COORDINATES = (43.7034, 7.2663)
THRESHOLD = 85

def add_info(row):
    url = row[0].rsplit('/',1)[1]
    req = urllib2.Request('http://aplicaciones.localidata.com/eldaSuit/place/id/%s?_view=list' % url)
    resp = urllib2.urlopen(req)
    # 200
    body = resp.read()
    result = json.loads(body)
    if len(result['result']['items']) > 0:
        if type(result['result']['items'][0]["geoLocation"]['lat']) == list:
            lat = float(result['result']['items'][0]["geoLocation"]['lat'][0])
        else:
            lat = float(result['result']['items'][0]["geoLocation"]['lat'])
        if type(result['result']['items'][0]["geoLocation"]['long']) == list:
            long_ = float(result['result']['items'][0]["geoLocation"]['long'][0])
        else:
            long_ = float(result['result']['items'][0]["geoLocation"]['long'])
        row.append((lat,long_))
    
        uri = row[3]
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT ?place ?placeLabel ?lat ?long
             WHERE {
            <%s> geo:lat ?lat.
            <%s> geo:long ?long.
            }
            """ % (uri,uri))        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for place in results['results']['bindings']:
            lat = float(place['lat']['value'])
            long_ = float(place['long']['value'])
            if vincenty(NICE_COORDINATES, (lat,long_)).km > 15:
                return False
        return True
    else:
        return False

with open('data/dbpedia_match_nogeo.csv','r') as input_fp:
    reader=csv.reader(input_fp,)
    # skip header
    reader.next()
    rows = [ [unicode(col,'utf-8') for col in row] for row in reader]

new_rows = []
for row in rows:
    #convert scoro to float
    row[4] = float(row[4])
    #add informations
    if add_info(row):
        new_rows.append(row)
        
with open('data/dbpedia_match_nogeo_coordinates.csv','wb') as output_fp:
    writer=csv.writer(output_fp,)
    # skip header
    writer.writerow(['3cixty_uri','3cixty_label','dbpedia_label','dbpedia_uri','score','coordinates'])
    for row in new_rows:
        row_utf8 = [s.encode('utf-8') if type(s) == unicode else s for s in row]
        writer.writerow(row_utf8)        
        
keys = set(map(lambda row : row[3], new_rows))
groups = [[row for row in new_rows if row[3] == key] for key in keys]
new_pois = []
for group in groups:
    best_score = max(group,key= lambda x: x[4])
    group = filter(lambda row: row[4] == best_score[4],group)
    group = filter(lambda row: row[4] > THRESHOLD, group)
    if len(group) >= 1:
        # keep nearest to center
        min_distance = float('inf')
        min_poi = None
        for row in group:
            distance = vincenty(NICE_COORDINATES, row[5]).km
            if distance < min_distance:
                min_distance = distance
                min_poi = row
        position = min_poi[5]
        min_poi[5] = position[0]
        min_poi.append(position[1])
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
        }
                    """ % (min_poi[3],min_poi[3]))        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for place in results['results']['bindings']:
            try:
                label = place['preferredLabel']['value']
            except KeyError:
                label = place['label']['value']
            min_poi[2] = label
        new_pois.append(min_poi)
        
new_pois = sorted(new_pois,key=lambda x: x[4],reverse=True)

with open('data/dbpedia_match_nogeo_distinct.csv','wb') as output_fp:
    writer=csv.writer(output_fp,)
    # skip header
    writer.writerow(['3cixty_uri','3cixty_label','dbpedia_label','dbpedia_uri','score','latitude','longitude'])
    for row in new_pois:
        row_utf8 = [s.encode('utf-8') if type(s) == unicode else s for s in row]
        writer.writerow(row_utf8)