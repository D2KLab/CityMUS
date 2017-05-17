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
# this set contains all resources downloaded
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

set_uri_known = set()
queue_uri_to_expand = collections.deque()

with open('resources_to_expand.csv','r') as input_fp:
    reader=csv.reader(input_fp,)
    set_uri_known = set([unicode(x[0],'utf-8') for x in reader])
count = len(set_uri_known)
count_processed_uri = 0
print(count)
for uri in set_uri_known:
    queue_uri_to_expand.append(uri)  
while len(queue_uri_to_expand) > 0:
    resource = queue_uri_to_expand.popleft()
    sparql.setQuery(
        """
select distinct ?c1 where {
<%s> <http://purl.org/dc/terms/subject> ?c1
}
        """ % resource)

    results = sparql.query().convert()
    count_processed_uri +=1
    print(count_processed_uri)
    for row in results['results']['bindings']:
        for column in row:
            if row[column]['value'] not in set_uri_known:
                set_uri_known.add(row[column]['value'])
                count +=1
                print(count)
                

print(len(set_uri_known))

with open('resources_expanded.csv','wb') as out_fp:
    csv_out=csv.writer(out_fp,)
    for row in set_uri_known:
        row_utf8 = row.encode('utf-8')
        csv_out.writerow([row_utf8])
