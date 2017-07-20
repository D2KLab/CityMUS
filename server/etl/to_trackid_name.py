
# coding: utf-8

# In[5]:

import json
from pprint import pprint

with open('../data/poi_artist_path.json','r') as input_fp:
    poi_artist_tracks = json.load(input_fp)


# In[6]:

tracks = dict()
for poi in poi_artist_tracks:
    for artist in poi_artist_tracks[poi]:
        for track in poi_artist_tracks[poi][artist]['tracks']:
            tracks[track[0]] = track[1]


# In[31]:

with open('../data/tracks.json','wb') as output_fp:
    json.dump(tracks,output_fp)

