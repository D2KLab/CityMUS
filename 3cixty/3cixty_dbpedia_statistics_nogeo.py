import json

with open('data/dbpedia_match_nogeo.json', 'r') as json_data:
    places = json.load(json_data)
    
    distinct_3cixty_uri = [x[0] for x in places]
    distinct_3cixty_names = [x[1] for x in places]
    distinct_dbpedia_names = [x[2] for x in places]
    distinct_dbpedia_uri = [x[3] for x in places]

    print(len(set([x[0] for x in places])))
    print(len(set([x[1] if type(x[1]) == unicode else x[1][0] for x in places])))

    print(len(set([x[2] for x in places])))
    print(len(set([x[3] for x in places])))