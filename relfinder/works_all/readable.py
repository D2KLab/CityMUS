
import re
import sys
import urllib2
query_wikidata_prop = """SELECT ?label WHERE {
  ?m ?p <STRING_TO_SUB>.
  ?m rdfs:label ?label.
  FILTER (lang(?label) = 'en') 
  FILTER (?m = wd:P190|| ?m= wd:P19 || ?m =wd:P86||?m =wd:P47||?m = wd:P495||?m = wd:P17||?m = wd:P136)
}
LIMIT 1"""



query_wikidata_ent = """SELECT ?label WHERE {
  <STRING_TO_SUB> rdfs:label ?label.
  FILTER (lang(?label) = 'en')                               
}
LIMIT 1"""

def getQueryResponse(query,endpointURL='http://dbpedia.org/sparql'):
    escapedQuery = urllib2.quote(query)
    requestURL = endpointURL + "?query=" + escapedQuery
    try:
        request = urllib2.Request(requestURL)
        result = urllib2.urlopen(request)
        res = result.read()
        return res
    except:
        raise Exception

all_lines_1 = open(sys.argv[1]).read().splitlines()

all_lines_2 = []

for l_1 in all_lines_1:
    items_1 = l_1.split('--->')
    items_2 = []
    for i in items_1:
        if 'wikidata' in i:
            if 'prop' in i:
                q = query_wikidata_prop.replace('STRING_TO_SUB',i)
            else:
                q = query_wikidata_ent.replace('STRING_TO_SUB',i)
            res = getQueryResponse(q,endpointURL='http://query.wikidata.org/sparql')
            print q
            i_2 = re.findall(r'<literal.*>(.*?)</literal>', res , re.S)[0]
            items_2.append(i_2)
    l_2 = '--->'.join(items_2)
    all_lines_2.append(l_2)

with open(sys.argv[2],'w+') as out:
        out.write("\n".join(all_lines_2))


        


