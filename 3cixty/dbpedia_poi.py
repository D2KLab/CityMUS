import re
from geopy.distance import vincenty
from unidecode import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint
import json
from SPARQLWrapper import SPARQLWrapper,JSON
import re
import Queue
import json
import collections
from geopy.distance import vincenty
from unidecode import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint
import json
from SPARQLWrapper import SPARQLWrapper,TURTLE,JSON
import time
import csv




sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    SELECT ?place ?placeLabel
     WHERE {
    ?place geo:lat ?lat.
    ?place geo:long ?long.
    ?place rdfs:label ?placeLabel.
    FILTER(
     xsd:double(?lat)  <= 43.80 &&
     xsd:double(?lat) >= 43.63 &&
     xsd:double(?long) <= 7.36 &&
     xsd:double(?long) >= 7.14
    )
    }
    """)        
sparql.setReturnFormat(JSON)
places = sparql.query().convert()

new_places = []
for place in places['results']['bindings']:
    uri = place['place']['value']
    label = place['placeLabel']['value']
    new_place = {}
    new_place['place'] = uri
    new_place['placeLabel'] = label
    new_places.append(new_place)    


#add places with second query

# this set contains all resources downloaded
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

distinct_dbpedia_category = set()
distinct_dbpedia_places = set()
queue = collections.deque()

distinct_dbpedia_category.add(u'http://dbpedia.org/resource/Category:Nice')
queue.append(u'http://dbpedia.org/resource/Category:Nice')
while len(queue) > 0:
    resource = queue.popleft()
    sparql.setQuery("""describe <%s>""" % resource)
    results = sparql.query().convert()
    for triple in results['results']['bindings']:
        if triple['o']['value'] == resource \
        and triple['p']['value'] == u"http://www.w3.org/2004/02/skos/core#broader" \
        and type(triple['s']['value']) == unicode \
        and triple['s']['value'].startswith("http://dbpedia.org/resource/Category:") \
        and triple['s']['value'].find('People') == -1:
            #print(triple['s']['value'])
            queue.append(triple['s']['value'])
            distinct_dbpedia_category.add(triple['s']['value'])
        elif triple['o']['value'] == resource \
        and triple['p']['value'] == u"http://purl.org/dc/terms/subject" \
        and type(triple['s']['value']) == unicode :
            distinct_dbpedia_places.add(triple['s']['value'])

final_poi = set()

for resource in distinct_dbpedia_places:
    sparql.setQuery("""
    select distinct ?uri where{

filter(?uri = <%s>).
{ ?uri a <http://dbpedia.org/ontology/Place> } 
UNION 
{ ?uri a <http://dbpedia.org/class/yago/YagoLegalActorGeo> }
UNION
{ ?uri a <http://dbpedia.org/class/yago/YagoPermanentlyLocatedEntity> }
minus 
{?uri a <http://dbpedia.org/ontology/Person>}
minus
{?uri a <http://dbpedia.org/class/yago/Person100007846>}
}
    """ % resource)
    results = sparql.query().convert()
    if len(results['results']['bindings']) > 0:
        final_poi.add(resource)

for resource in final_poi:
    sparql.setQuery("""
    SELECT ?place ?placeLabel
     WHERE {
    filter(?place = <%s>).
    ?place rdfs:label ?placeLabel.
    
    }
    """ % resource)        
    sparql.setReturnFormat(JSON)
    places = sparql.query().convert()

    for place in places['results']['bindings']:
        uri = place['place']['value']
        label = place['placeLabel']['value']
        new_place = {}
        new_place['place'] = uri
        new_place['placeLabel'] = label
        new_places.append(new_place)    


with open('data/dbpedia_poi_nogeo.json', 'w') as outfile:
    print(new_places)
    json.dump(new_places, outfile)
    print("Dbpedia names: %d" % len(new_places))