import json
import csv
with open('source_data/dbpedia_poi_match.json', 'r') as pois:
    with open('source_data/1_6_doremus_dbpedia_works.csv', 'r') as works:
        with open('source_data/1_7_doremus_dbpedia_artists.csv', 'r') as artists:
            with open('resources_to_expand.csv','w') as out_fp:
                places = json.load(pois)
                distinct_dbpedia_uri = set([x[3] for x in places])

                reader=csv.reader(artists,)
                next(reader, None)  # skip the headers
    
                distinct_dbpedia_uri |= set([unicode(x[1],'utf-8') for x in reader])
                reader=csv.reader(works,)
                next(reader, None)  # skip the headers

                distinct_dbpedia_uri |= set([unicode(x[1],'utf-8') for x in reader])

                csv_out=csv.writer(out_fp,)
                for row in distinct_dbpedia_uri:
                    row_utf8 = row.encode('utf-8')
                    csv_out.writerow([row_utf8])
