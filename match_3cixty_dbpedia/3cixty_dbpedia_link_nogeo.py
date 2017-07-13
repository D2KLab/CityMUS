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

NICE_reg = re.compile(r'.*nice.*',re.IGNORECASE)
ONLY_NICE_reg = re.compile(r'^\s?nice\s?$',re.IGNORECASE)

MIN_SCORE = 80

def best_match_2(match_src,match_dest):
    match_func = [fuzz.WRatio,fuzz.partial_ratio,fuzz.partial_token_sort_ratio,fuzz.token_set_ratio,fuzz.token_sort_ratio]
    results = [process.extractOne(match_src,list(match_dest), scorer= func) for func in match_func]
    final_result = []
    for result in results:
        result_string = result[0]
        tmp = [process.extractOne(match_src,[result_string], scorer= func) for func in match_func]
        scores = [x[1] for x in tmp]
        mean = float(sum(scores))/len(scores)
        final_result.append((result_string,mean))
    match,mean = max(final_result,key=lambda x: x[1])
    return (match,mean)

dbpedia_match =[]
    
with open('data/dbpedia_poi_nogeo.json', 'r') as json_data:
    wiki_places = json.load(json_data)
    ascii_uri = {}
    for place in wiki_places:
        ascii_label = unidecode(place['placeLabel'])
        ascii_label = ascii_label if bool(NICE_reg.search(ascii_label)) else ascii_label + ' nice'
        place['ascii'] = ascii_label
        ascii_uri[ascii_label] = place
        
with open('data/3cixty_places_dump.json', 'r') as json_data:
    cixty_places = json.load(json_data)
    for place in cixty_places:
        label = place['label'] if type(place['label']) == unicode else place['label'][0]
        filtered_wiki_places = wiki_places

        if len(filtered_wiki_places) > 0:
            match_src = unidecode(label)
            if bool(NICE_reg.search(match_src)) == False:
                match_src = match_src + ' nice'
                
            match_dest = [wiki_place['ascii'] for wiki_place in filtered_wiki_places]
            
            match,score = best_match_2(match_src,match_dest)
            if score > MIN_SCORE :
                if bool(ONLY_NICE_reg.search(match)) == True and bool(ONLY_NICE_reg.search(label)) == False:
                    continue
                    #pass
                
                match_place = ascii_uri[match]
                # 3cixty uri, 3cixty label, dbpedia uri, dbpedia label, score
                dbpedia_match.append((place['_about'],place['label'],match_place['placeLabel'],match_place['place'],score))
                print(label,match_place['placeLabel'],score) 

print(len(dbpedia_match))

import csv
dbpedia_match_sorted = sorted(dbpedia_match, reverse=True, key=lambda x: x[4])
with open('data/dbpedia_match_nogeo.csv','wb') as out:
    csv_out=csv.writer(out,)
    csv_out.writerow(['3cixty_uri','3cixty_label','dbpedia_label','dbpedia_uri','score'])
    for row in dbpedia_match_sorted:
        row_utf8 = [s.encode('utf-8') if type(s) == unicode else s for s in row]
        csv_out.writerow(row_utf8)
        
with open('data/dbpedia_match_nogeo.json','wb') as out:
    json.dump(dbpedia_match_sorted,out)