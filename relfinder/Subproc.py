#!/usr/bin/python
import csv
import re
import urllib2
import os
from os import listdir
from os.path import isfile, join
import Queue
import threading
from datetime import datetime
import subprocess
import pandas as pd
import sys
import json
import time

def createLine(text):
    lines = text.split('\n')
    return "".join([l.strip() for l in lines])


def t_func(queue,lock,output_path,POI_list,total_works,writer,max_depth):
    mynum = threading._get_ident()
    while 1:
        try:
            row = queue.get_nowait()
        except Queue.Empty:
            return 0
        else :
            file_name = str(row[0])
            w= row[1]
            endpoint = row[2]
            names_list = []
            ind_p  = 0
            for p in POI_list:
                out = subprocess.check_output(["php","-f","test.php",w,p,endpoint,max_depth])
                results = re.findall(r'<result>.*?</result>', out, re.S)
                if len(results)>0:
                    xml = "\n".join([createLine(r) for r in results])
                    final_name = file_name + '_' + str(ind_p)
                    storage_file =  output_path + final_name
                    f =  open(storage_file , "wb")
                    f.write(xml)
                    f.close()
                    names_list.append(file_name)
                ind_p += 1
            all_files = '|||'.join(names_list)
            lock.acquire()
            writer.writerow(row+(all_files,))
            lock.release()




# Simple command

#"<http://dbpedia.org/resource/Nice>"
if len(sys.argv) != 4:
    print "\nYou have to specify 3 arguments: \n\t1) Compositions file\n\t2) POIs file\n\t3) Number of threads\n"
    sys.exit(0)

if not os.path.exists("output_files/"):
    os.makedirs("output_files/")

df1 = pd.read_csv(sys.argv[1])
works_list = df1[df1.columns[1]]
poi_filepath = sys.argv[2]
if "Nice" == poi_filepath:
    max_depth = '4'
    if 'wikidata' in poi_filepath:
        output_path = 'output_files/all_links_wikidata_Nice/'
        trace_path = 'output_files/already_done_wikidata_Nice.csv'
        endpoint = "https://query.wikidata.org/sparql"
        POI_list = ["http://www.wikidata.org/entity/Q33959"]
    else:
        output_path = 'output_files/all_links_dbpedia_Nice/'
        trace_path = 'output_files/already_done_dbpedia_Nice.csv'
        endpoint = "https://dbpedia.org/sparql"
        POI_list = ["http://dbpedia.org/resource/Nice","http://dbpedia.org/resource/Category:Nice"]
else:
    max_depth = '3'
    df2 = pd.read_csv(poi_filepath)
    if 'wikidata' in poi_filepath:
        df2['clean_score'] = df2['score'].apply(lambda x:float(x[0:-3]))
        df2 = df2[(df2.clean_score >= 90.0)]
        output_path = 'output_files/all_links_wikidata/'
        trace_path = 'output_files/already_done_wikidata.csv'
        endpoint = "https://query.wikidata.org/sparql"
        POI_list = df2[df2.columns[3]].drop_duplicates()
    else:
        output_path = 'output_files/all_links_dbpedia/'
        trace_path = 'output_files/already_done_dbpedia.csv'
        endpoint = "https://dbpedia.org/sparql"
        POI_list = df2[df2.columns[0]]

#POI_list = pd.read_csv(sys.argv[2])[0]
#POI_list = ["http://dbpedia.org/resource/Nice"]
n_threads = int(sys.argv[3])

try:
    all_lines =[l.replace('\n','') for l in open(trace_file,'r+').readlines()]
except:
    all_lines = []
if not os.path.exists(output_path):
    os.makedirs(output_path)
    onlyfiles = []
else:
    onlyfiles = [f for f in listdir(output_path) if isfile(join(output_path, f))]


lock = threading.Lock()
queue = Queue.Queue()
files = []



try:
    with open(trace_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            files.append(row[0])
except:
    files = []


ind = 0
for w in works_list:
    if ind not in files:
        t = (ind,w,endpoint)
        queue.put(t)
    ind += 1
 

total_works = len(works_list)

trace_file = open(trace_path,'a+')
writer = csv.writer(trace_file)

ts = time.time()
print 'START TIME: '+datetime.fromtimestamp(ts).strftime('%H:%M:%S')

for u in range(n_threads):
    t = threading.Thread(target=t_func, args = (queue,lock,output_path,POI_list,total_works,writer,max_depth))
    t.start()

count_threads = threading.activeCount()
while count_threads > 1:
    sz = queue.qsize()
    print "Queue size: "+str(sz)
    now = total_works - sz - count_threads
    if now < 0:
        now = 0
    done = (100.0 * now)/total_works
    print "Completed: "+str(done)+"%"
    time.sleep(120)
    ts = time.time()
    print 'TIME: '+datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    count_threads = threading.activeCount()
    print "Active threads: "+ str(count_threads)

ts = time.time()
print 'END TIME: '+datetime.fromtimestamp(ts).strftime('%H:%M:%S')

