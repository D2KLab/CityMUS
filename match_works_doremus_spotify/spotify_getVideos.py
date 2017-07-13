#!/usr/bin/python
import json
import csv
import sys
import re
import urllib2
import os
from os import listdir
from os.path import isfile, join
import Queue
import threading
import spotipy
from datetime import datetime


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console

sp = spotipy.Spotify()


def spotify_search(term):
    results = sp.search(q=term, limit=20)
    tracks = results['tracks']['items']
    return tracks


def getItems(names_doremus,composers_doremus):
    result = []
    for n in names_doremus:
            composers = composers_doremus.replace('|||',' ')
            term = n +' '+composers
            result = spotify_search(term)
            if len(result)>0:
                break
    
    if len(result) == 0:
        flag = True
        for n in names_doremus:
            composers = composers_doremus.split('|||')
            if flag:
                for c in composers:
                    term = n +' '+c
                    result= spotify_search(term)
                    if len(result)>0:
                        flag = False
                        break
            else:
                break

    for term in names_doremus:
            result = spotify_search(term)
            if len(result)>0:
                break

    return result

def t_func(queue,lock,output_path):
    mynum = threading._get_ident()
    while 1:
        try:
            row = queue.get_nowait()
        except Queue.Empty:
            lock.acquire()
            #Handle empty queue here
            print "END"
            lock.release()
            return 0
        else :
            data = {}
            sz = queue.qsize()
            if sz % 50 == 0:
                lock.acquire()
                print "Remaining: "+str(queue.qsize())
                now = datetime.now()
                s = '%d:%d:%d'%(now.hour,now.minute,now.second)
                print "Time: "+s
                lock.release()
            uri_doremus = row[1]
            names_doremus = row[2].split('|||')
            storage_file = output_path+row[5]
            composers_doremus = row[6]
            try:
                data = getItems(names_doremus,composers_doremus)
                with open(storage_file,'w+') as outfile:
                    json.dump(data,outfile)
            except:
                lock.acquire()
                print 'Request Error'
                lock.release()



            

input_path= sys.argv[1]
if len(sys.argv) > 2:
    N1 = int(sys.argv[2])
    N2 = int(sys.argv[3])
else:
    N1 = 1
    N2 = 200000

output_path = 'all_links/'
if not os.path.exists(output_path):
    os.makedirs(output_path)
    onlyfiles = []
else:
    onlyfiles = [f for f in listdir(output_path) if isfile(join(output_path, f))]



lock = threading.Lock()
mylines = Queue.Queue()

count = 0
with open(input_path, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if count >= N1 and count<N2:
            fl = row[5]
            if fl not in onlyfiles:
                mylines.put(row)
        if count % 10000 == 0:
            print count
        count += 1


for u in range(1):
    t = threading.Thread(target=t_func, args = (mylines,lock,output_path))
    t.start()





