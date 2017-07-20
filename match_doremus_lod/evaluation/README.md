# Evaluation

Evaluate DBpedia and Wikidata artist matching with DOREMUS artists, comparing them with results provided by ISNI

## Dependencies:
* pprint
* numpy
* sparqlwrapper
* pandas
* sklearn
* matplotlib

      pip3 install pprint numpy pandas sklearn matplotlib
      pip3 install git+https://github.com/rdflib/sparqlwrapper#egg=sparqlwrapper

## File required:
* doremus_dbpedia_artists.csv
* doremus_wikidata_artists.csv

## Running

open and run 'evaluation.ipynb' notebook


## Output

Output files contains images with useful statistics and csv containing artists that are matched differently by our algorithm and ISNI
