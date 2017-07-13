
# coding: utf-8

# In[26]:

import csv
import json
with open('final_paths.csv','r') as input_fp:
    reader=csv.reader(input_fp,)
    # skip header
    reader.next()
    rows = [ [unicode(col,'utf-8') for col in row] for row in reader]

with open('artists_tracks.json','r') as input_fp:    
    artists = json.load(input_fp)    
    


# In[28]:

poi_artist_path = dict()
for row in rows:
    poi_artist_path[row[12]] = dict()

for row in rows:
    if len(poi_artist_path[row[12]]) < 5:
        try:
            if row[0] in artists:
                poi_artist_path[row[12]][row[0]]
        except KeyError:
            path_tracks = dict()
            path = row[:13]
            tracks = artists[row[0]]['tracks']
            path_tracks['path'] = path
            path_tracks['tracks'] = tracks
            print(len(tracks))
            poi_artist_path[row[12]][row[0]] = path_tracks


# In[24]:

artists


# In[20]:

poi_artist_path


# In[29]:

with open('poi_artist_path.json','wb') as output_fp:
    json.dump(poi_artist_path,output_fp)

