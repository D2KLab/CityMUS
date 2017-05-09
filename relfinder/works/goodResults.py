import csv
import sys

def evaluateQuality(row):
    goods = []
    if '&&&1' in row[1]:
        work_uri = row[0]
        paths = row[1].split('|||')
        poi_uri = row[2]
        for p in paths:
            if '&&&1' in p:
                goods.append(work_uri+'--->'+p.replace('&&&1','')+'--->'+poi_uri)
    return goods
all_tuples = []
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count > 0:
            res = evaluateQuality(row)
            if len(res)>0:
                all_tuples += res
        count += 1

with open(sys.argv[2],'w+') as out:
        out.write("\n".join(all_tuples))