# CityMusic

The experience of a walk in the city with the most suitable soundtrack, on the base of the urban context.

## Abstract

Linked Data make possible the discovering of interesting connection between semantic entities that belongs to different domains. This report contains all the material we realised for developing **_cityMus_**, a web application that gives to the user the experience of a walk in the city with the most suitable soundtrack, on the base of the urban context. The application relies on a recommender system that search the shorter path in the graph between the _Points of Interest_ (PoIs) nearby the user and music composers, making use of a combination of [DBpedia](http://dbpedia.org) and domain-specific datasets like [3cixty](http://3cixty.eurecom.fr/) for tourism and [DOREMUS](http://doremus.org) for music metadata.

## Content of the repository

##### Knowledge base matching
* `3cixty` Match PoIs between 3cixty and DBpedia.
* `artist_to_spotify` Match Artists between DOREMUS and Spotify.
* `artist_to_spotify` Match Artists between DOREMUS and Spotify.
* `matching_DB_Doremus`
* `matching_performances`
* `spotify_analytic`
* `spotify_api` Match DOREMUS works to Spotify tracks.
* `youtube_api` Match DOREMUS works to YouTube music videos.


##### Path finding

* `pathfinding` A script for computing the shortest paths in a RDF graph.
* `relfinder`
* `Artists_POIs_PathDiscovering`

##### Application
* `app` The client application.
* `server` The recommender API server.

##### Other

* `report` The final report of the project ([pdf](./report/report.pdf)).
