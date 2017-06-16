import collections
import csv
import json
import sys
from os import listdir
from os.path import isfile, join

output_path =sys.argv[1]

categories ={1:"low",2:"medium",3:"medium_high",5:"high"}

print output_path

if 'dbpedia' in output_path and 'artists' in output_path:
    print 1
    input_path = sys.argv[2]
    data = json.load(open(input_path))
    arr = []
    for key in data:
        uri_doremus = key.encode('utf-8')
        rank = data[key]["rank"]
        uri_dbpedia = data[key]["best"].encode('utf-8')
        arr.append((uri_doremus,uri_dbpedia,rank))
    arr.sort(key=lambda tup: -tup[2])
    with open('RESULTS/'+output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(('uri_doremus','uri_dbpedia','rank'))
        for t in arr:
            category = ""
            writer.writerow(t)
    dic = {}
    for key in data:
        rank = data[key]["rank"]
        rank = round(rank, 1)
        if rank in dic:
            dic[rank] = dic[rank] + 1
        else:
            dic[rank] = 0
    odic = collections.OrderedDict(sorted(dic.items()))
    with open(output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("score","count","category"))
        for k in odic:
            category = ""
            for c in categories:
                if k < c:
                    category = categories[c]
                    break
            t = (k,odic[k],category)
            writer.writerow(t)


elif 'dbpedia' in output_path and 'works' in output_path:
    print 2
    input_path = sys.argv[2]
    data = json.load(open(input_path))
    arr = []
    for key in data:
        uri_doremus = key.encode('utf-8')
        rank = data[key]["rank"]
        uri_dbpedia = data[key]["best"].encode('utf-8')
        arr.append((uri_doremus,uri_dbpedia,rank))
    arr.sort(key=lambda tup: -tup[2])
    with open('RESULTS/'+output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(('uri_doremus','uri_dbpedia','rank'))
        for t in arr:
            category = ""
            writer.writerow(t)
    dic = {}
    for key in data:
        rank = data[key]["rank"]
        rank = round(rank, 1)
        if rank in dic:
            dic[rank] = dic[rank] + 1
        else:
            dic[rank] = 0
    odic = collections.OrderedDict(sorted(dic.items()))
    with open(output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("score","count","category"))
        for k in odic:
            category = ""
            for c in categories:
                if k < c:
                    category = categories[c]
                    break
            t = (k,odic[k],category)
            writer.writerow(t)





elif 'wikidata' in output_path and 'artists' in output_path:
    print 3
    mypath = 'artists/wikidata/all_links/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    doremus_prefix = "http://data.doremus.org/artist/"
    tot_tuples = []
    dic = {}
    for p in onlyfiles:
        doremus_uri = doremus_prefix+p
        #writer.writerow(("uri_wikidata","name_score","born_score","death_score","total_score"))
        with open(mypath+p, 'rb') as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if count > 0:
                    t = (doremus_uri,) + tuple(row)
                    tot_tuples.append(t)
                    rank = float(t[5])
                    #print rank
                    rank = round(rank, 1)
                    if rank in dic:
                        dic[rank] = dic[rank] + 1
                    else:
                        dic[rank] = 0
                count += 1
    tot_tuples.sort(key=lambda tup: -float(tup[5]))
    odic = collections.OrderedDict(sorted(dic.items()))
    with open('RESULTS/'+output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("uri_doremus","uri_wikidata","name_score","born_score","death_score","total_score"))
        for t in tot_tuples:
            writer.writerow(t)
    with open(output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("score","count","category"))
        for k in odic:
            category = ""
            for c in categories:
                if k < c:
                    category = categories[c]
                    break
            t = (k,odic[k],category)
            writer.writerow(t)
        







elif 'wikidata' in output_path and 'works' in output_path:
    print 4
    mypath = 'compositions/wikidata/all_links/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    doremus_prefix = "http://data.doremus.org/expression/"
    tot_tuples = []
    dic = {}
    for p in onlyfiles:
        doremus_uri = doremus_prefix+p
        g = onlyfiles.index(p)
        if g % 1000 == 0:
            print g
        #writer.writerow(("uri_wikidata","name_score","born_score","death_score","total_score"))
        with open(mypath+p, 'rb') as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if count > 0:
                    t = (doremus_uri,) + tuple(row)
                    tot_tuples.append(t)
                    rank = float(t[5])
                    rank = round(rank, 1)
                    if rank in dic:
                        dic[rank] = dic[rank] + 1
                    else:
                        dic[rank] = 0
                count += 1
    tot_tuples.sort(key=lambda tup: -float(tup[5]))
    odic = collections.OrderedDict(sorted(dic.items()))
    with open('RESULTS/'+output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("uri_doremus","uri_wikidata","title_score","year_score","composer_score","total_score"))
        for t in tot_tuples:
            writer.writerow(t)
    with open(output_path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(("score","count","category"))
        for k in odic:
            category = ""
            for c in categories:
                if k < c:
                    category = categories[c]
                    break
            t = (k,odic[k],category)
            writer.writerow(t)

