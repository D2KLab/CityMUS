with open('../data/dbpedia_match_nogeo_distinct.csv','r') as input_fp:
    reader=csv.reader(input_fp,)
    # skip header
    reader.next()
    rows = [ [unicode(col,'utf-8') for col in row] for row in reader]