# DOREMUS Relfinder

To link find paths between works and POIs, we are trying to use Relfinder both for Dbpedia and Wikidata.
The script that performs this action is called `SubProc.py`. It can perform different operation depending
on the command line arguments passed to.
It takes as input file one or two files in the folder `input_files` and it writes new files in the folder `output_files` 
that is created when the script runs for the first time. Then it is possible to stop running and continue the execution
in the future. The script automatically keeps trace of the work already done.

## Problems and alternatives

Trying running the script, we have noted that it takes a very long time. In fact:

* We have k works, where **k** is a number comprised between 5000 and 40000 depending on the filtering accuracy and on the used ontology (Dbpedia or Wikidata)
* For each of them, we have to laung Relfinder **n** times, where **n** is the number of POIs (between 80-200)
* Totally we have to launch **n** * **k** times Relfinder
* For every relfinder launch, there is a number of queries, proportional to the max explored depth

As you can deduce, when the number of works and POIs is high, the algorithm is too slow. To solve this problem we thought to not pass to Relfinder the POIs but to pass the Nice entity, increasing the max depth. This suggestion is justified by the hyphotesis that every POI should be linked with Nice, being a Nice POI. Teorically this is true, but we have noted that in Wikidata some POIs are not linked with Nice and in Dbpedia some POIs are too far from the Nice entity. However these are a minority, so we think that this is a good alternative. As Nice entity, we'll use:


* the entity [Nice Wikidata](http://www.wikidata.org/entity/Q33959) for Wikidata
* the entity [Nice Dbpedia](http://dbpedia.org/resource/Nice) or [Nice Category Dbpedia](http://dbpedia.org/resource/Category:Nice)  for DBpedia



![Diagram](Concept_diagram.png)





## Description of the arguments

| Number | Description | Example
|---|---|---|
|`Input works file` |It is the file where are contained all matched works, in the  |kdkdk
