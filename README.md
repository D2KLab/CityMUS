# CityMusic

The experience of a walk in the city with the most suitable soundtrack, on the base of the urban context.

## Abstract

Linked Data make possible the discovering of interesting connection between semantic entities that belongs to different domains. This report contains all the material we realised for developing **_cityMus_**, a web application that gives to the user the experience of a walk in the city with the most suitable soundtrack, on the base of the urban context. The application relies on a recommender system that search the shorter path in the graph between the _Points of Interest_ (PoIs) nearby the user and music composers, making use of a combination of [DBpedia](http://dbpedia.org) and domain-specific datasets like [3cixty](http://3cixty.eurecom.fr/) for tourism and [DOREMUS](http://doremus.org) for music metadata.

## Content of the repository

##### Knowledge base matching
* `match_3cixty_dbpedia` Match PoIs between 3cixty and DBpedia.
* `match_artist_doremus_spotify` Match Artists between DOREMUS and Spotify.
* `match_doremus_lod` Match artists between DOREMUS and DBpedia/Wikidata -- see [stats](./match_doremus_lod/evaluation/v1/check_performance.ipynb).
* `spotify_analytic`
* `match_works_doremus_spotify` Match DOREMUS works to Spotify tracks.
* `youtube_experiment` Use YouTube API for getting location related music videos.

##### Path finding

* `path finder` A script for computing the shortest paths in a RDF graph, in the form of a _python notebook_.

##### Application
* `app` The client application.
* `server` The recommender API server.

##### Other

* `report` The final report of the project ([pdf](./report/report.pdf)).
