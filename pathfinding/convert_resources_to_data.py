import csv

with open('resources_expanded.csv','r') as in_fp:
    with open('data_to_download.csv','w') as out_fp:
        reader=csv.reader(in_fp,)
        uris = [unicode(x[0],'utf-8') for x in reader]
        uris_rdf = set([(uri.encode("UTF-8") + '.rdf').replace('http://dbpedia.org/resource/', 'http://dbpedia.org/data/',1) for uri in uris])
        csv_out=csv.writer(out_fp,)
        for row in uris_rdf:
            csv_out.writerow([row])
