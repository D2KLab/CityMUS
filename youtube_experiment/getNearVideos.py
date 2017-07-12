import json
import csv
import sys
import re
import urllib2
import os

query = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&location=LATITUDE%2C+LONGITUDE&locationRadius=METER_RADIUSm&key=AIzaSyC3U8ZqKiCjaR9xSzXXG2_lpZJ3unm2GG8"
directory  = 'songs_for_position/'

def getFinalQuery(latitude,longitude,radius,query):
    s1 = query.replace('LATITUDE',latitude)
    s2 = s1.replace('LONGITUDE',longitude)
    s3 = s2.replace('METER_RADIUS',radius)
    return s3

def getResponse(url):
    req = urllib2.Request(url)
    out = urllib2.urlopen(req)
    d = out.read()
    data = json.loads(d)
    return data

try:
    latitude = sys.argv[1]
    longitude = sys.argv[2]
    s = latitude+longitude
    file_path = s.replace('.','_')
except:
    print "You should insert 2 arguments to launch the script coorectyl, the firts is the latitude and the second is the longitude"
else:
    if not os.path.exists(directory):
        os.makedirs(directory)
    youtube_identifiers = [] 
    if len(sys.argv)>3:
        radius = sys.argv[3]
    else:
        radius = '100'
    request_counter = 0
    start_url = getFinalQuery(latitude,longitude,radius,query)
    data = getResponse(start_url)
    count = 0

    while "nextPageToken" in data:
        items = data["items"]
        for item in items:
            identifier = item["id"]["videoId"]
            youtube_identifiers.append(identifier)
        next_token = data["nextPageToken"]
        url = start_url + '&pageToken='+next_token
        data = getResponse(url)
        count += 1
        print count

    print youtube_identifiers

    output_path = directory + file_path + '.json'
    with open(output_path,'w+') as outfile:
        json.dump(youtube_identifiers,outfile)
    

    

    



