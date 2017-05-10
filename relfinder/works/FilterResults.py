import csv
import sys
import pandas as pd
import re

from os import listdir
from os.path import isfile, join


trace_path = sys.argv[1]
output_path = sys.argv[2]

if 'wikidata' in trace_path:
    df2 = pd.read_csv("input_files/3cixty_wikidata_match.csv")
    df2['clean_score'] = df2['score'].apply(lambda x:float(x[0:-3]))
    df2 = df2[(df2.clean_score >= 90.0)]
    poi_entities = ["http://www.wikidata.org/entity/Q33959"] 
    POI_list = df2[df2.columns[3]].drop_duplicates()
    storage_folder = "output_files/all_links_wikidata_Nice/"
else:
    df2 = pd.read_csv("input_files/3cixty_dbpedia_match.csv")
    POI_list = df2[df2.columns[0]].drop_duplicates()
    poi_entities = ["http://dbpedia.org/resource/Nice","http://dbpedia.org/resource/Category:Nice"]
    storage_folder = "output_files/all_links_dbpedia_Nice/"

uri_dict = {}

with open(trace_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        id_uri = row[0]
        db_uri = row[1]
        uri_dict[id_uri] = db_uri

all_output_paths = [f for f in listdir(storage_folder) if isfile(join(storage_folder, f))]
print all_output_paths
all_tuples = []
count = 0
print "start"
c = 0
for o in all_output_paths:
    if c % 100 ==0:
        print c
    c += 1
    f = storage_folder+o
    id_uri = o.split("_")[0]
    poi_entity_index = int(o.split("_")[1])
    uri = uri_dict[id_uri]
    all_paths = []
    all_lines = open(f).read().splitlines()
    for line in all_lines:
        path = "--->".join(re.findall(r'<uri>(.*?)</uri>', line , re.S))
        quality = "0"
        for poi in POI_list:
            if poi in path:
                quality = "1"
                count +=1
                break
        all_paths.append(path+"&&&"+quality)
    all_paths_string = "|||".join(all_paths)
    t = (uri,all_paths_string,poi_entities[poi_entity_index])
    all_tuples.append(t)

with open(output_path,'w+') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(('work','path','poi'))
    for row in all_tuples:
        csv_out.writerow(row)

        
print count