# 3cixty dbpedia match

To link the 3cixty pois with dbpedia pois, we download all Nice pois in 3cixty and Dbpedia, then we match them usign their position and name similarity.
We wrote a script to download the 3cixty pois and one that download dbpedia pois and does the match.

## Installation

Dependencies:
* [Python 2.7.13](https://www.python.org/downloads/) (not the version 3)
* [_pip_ library](https://pip.pypa.io/en/stable/installing/)

      curl -O https://bootstrap.pypa.io/get-pip.py
      python get-pip.py

* python modules
      
      pip install spotipy
      pip install geopy
      pip install unidecode
      pip install fuzzywuzzy
      pip install pprint
      pip install sparqlwrapper

## Running

> In order to run the two provided script, it's necessary to create the data directory
      
      mkdir data 


For running the script:

    python 3cixty_dump.py
    python 3cixty_dbpedia.py 


### Output

Running the script, some messages are printed on the screen but are only verbose stuff.

The real output is the csv file dbpedia_match.csv

| 3cixty_uri | 3cixty_label | dbpedia_label | dbpedia_uri |score|
|---|---|---|---|---|
|http://data.linkedevents.org/location/c5e5c428-0342-330e-be99-351a9c1c936f|	Avenue Jean Médecin	|Avenue Jean-Médecin	|http://dbpedia.org/resource/Avenue_Jean_Médecin	|100.00.00|
