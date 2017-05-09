<?

require_once('RelationFinder.php');


$r = new RelationFinder();
$object1 = "<".$argv[1].">";
$object2 = "<".$argv[2].">";
//"<http://dbpedia.org/resource/Nice>";
//"<".$uri.">"
//$object1 = "a";
//$object2 = "b";
$maxDistance = intval($argv[4]);
$limit = 10;
$ignoredObjects;
$ignoredProperties= array(
	'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 
	'http://www.w3.org/2004/02/skos/core#subject',
	'http://dbpedia.org/property/wikiPageUsesTemplate',
	'http://dbpedia.org/property/wordnet_type'
	
	);

$avoidCycles = 2;

$arr = $r->getQueries($object1, $object2, $maxDistance, $limit, $ignoredObjects, $ignoredProperties, $avoidCycles);
//print_r($arr);

foreach ($arr as $distance){
	foreach ($distance as $query){
		$now = microtime(true);
		#echo "<xmp>".$query."</xmp>";
		$endpoint = $argv[3];
		#echo $endpoint;
		echo $r->executeSparqlQuery($query,$endpoint,"XML");
		//echo "<br>needed ".(microtime(true)-$now)." seconds<br>";
	}
}

