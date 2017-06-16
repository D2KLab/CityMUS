import urllib2
import geocoder
import re
import os
import os.path
import json

def computeProb(number,start,end):
    if number < 20:
        return float(number**2)/400
    elif end - number < 6:
        diff = end - number 
        return 1.0 - 4/float(diff)
    else:
        return 1

def StringMatching(str1,str2,op):
    c1 = str1.upper()==str2.upper()
    c1_cs = str1==str2
    c2 = re.search(str1, str2, re.IGNORECASE)
    c3 = re.search(str2, str1, re.IGNORECASE)
    c2_cs = re.search(str1, str2)
    c3_cs = re.search(str2, str1)
    if op == 'equal':
        return c1
    elif op == 'equal_cs':
        return c1_cs
    elif op == 'contains':
        return c1 or c2 or c3
    elif op == 'contains_cs':
        return c1_s or c2_s or c3_s

def isInText(term,text):
    if term in text:
        return 1.0
    else:
        terms = term.split(' ')
        n_terms = len(terms)
        vote = 0.0
        for t in terms:
            if t in text:
                vote += 1.0
        penalty = 0.1 + 0.2/n_terms
        if vote > 0.0:
            return vote/n_terms - penalty
        else:
            return vote

def YearDistance(year_1,year_2):
    distance = float(abs(int(year_1) - int(year_2)))
    if distance == 0.0:
        return 1.0
    else:
        d = 1/distance
        if d > 0.7:
            return 0.7
        else:
            return 1/distance
    


def JSONtoDictionary(path):
    json_data=open(path)
    data = json.load(json_data)
    final_dict = {}
    if 'dbpedia' in path:
        res = data["results"]["bindings"]
        for r in res:
            uri = r["s"]["value"].encode('utf-8') 
            names_u = r["labels"]["value"].split('|||')
            for name_u in names_u:
                name = name_u.encode('utf-8')
                final_dict[name] = uri
    elif 'wikidata' in path:
        for r in data:
            uri = r["s"].encode('utf-8')
            names_u = r["labels"]["value"].split('|||')
            for name_u in names_u:
                name = name_u.encode('utf-8')
                final_dict[name] = uri
    return final_dict        


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


def withoutSpecificChar(word,ch):
    if word[0] == ch:
        word = word[1:]
    if word[-1] == ch:
        word = word[0:-1]
    return word
    

def parseAndGetUris(lines,op="uri"):
    uri = []
    literal = []
    for line in lines:
        if op == "uri":
            if "<uri>" in line:
                uri.append(re.search('<uri.*>(.*)<.uri>',line).group(1))
        elif op == "literal":
            if "<literal>" in line:
                literal.append(re.search('<literal.*>(.*)<.literal>',line).group(1))
        elif op == "all":
            if "<literal>" in line:
                literal.append(re.search('<literal.*>(.*)<.literal>',line).group(1))
            if "<uri>" in line:
                uri.append(re.search('<uri.*>(.*)<.uri>',line).group(1))
    if "all": 
        return {uri[i]:literal[i] for i in range(len(uri))}
    if "uri":
        return uri
    if "literal":
        return literal


def getOutputFile(PATH):
    f = open(PATH,'a+')
    array_f = open(PATH).readlines()
    if len(array_f) > 0:
        try:
            last = array_f[-1]
            offset = int(last.split('|||')[0])+1
        except:
            offset = len(array_f)
    else:
        offset = 0
    return f,offset


def htmlDecode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s
