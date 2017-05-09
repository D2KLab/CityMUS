#!/usr/bin/python
import csv
import pandas as pd
import sys

# Simple command

#"<http://dbpedia.org/resource/Nice>"

df_1 = pd.read_csv(sys.argv[1])
df_2 = pd.read_csv(sys.argv[2])
works_list = df_1[df_1.columns[1]]
POI_list = df_2[df_2.columns[1]]



with open(sys.argv[3], 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(('index','work','poi'))
    count = 0
    for w in works_list:
        for p in POI_list:
            t = (count,w,p)
            writer.writerow(t)
            count +=1