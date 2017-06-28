
# coding: utf-8

# In[2]:

import csv
import json
with open('../data/final_paths.csv','r') as input_fp:
    reader=csv.reader(input_fp,)
    # skip header
    reader.next()
    rows = [ [unicode(col,'utf-8') for col in row] for row in reader]


# In[26]:

poi_artist_path = dict()
for row in rows:
    poi_artist_path[row[12]] = dict()


# In[27]:

for row in rows:
    if len(poi_artist_path[row[12]]) < 5:
        try:
            poi_artist_path[row[12]][row[0]]
        except KeyError:
            poi_artist_path[row[12]][row[0]] = row


# In[30]:

with open('../data/poi_artist_path.json','wb') as output_fp:
    json.dump(poi_artist_path,output_fp)

