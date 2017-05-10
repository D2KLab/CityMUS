
import urllib2
s = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT * WHERE {
?of1 ?pf1 <http://dbpedia.org/resource/Rome> . 
?middle ?pf2 ?of1 . 
?middle ?ps1 <http://dbpedia.org/resource/Lazio> . 

FILTER ((?pf1 != rdf:type ) && 
(?pf1 != skos:subject ) && 
(?pf1 != <http://dbpedia.org/property/wikiPageUsesTemplate> ) && 
(?pf1 != <http://dbpedia.org/property/wordnet_type> ) && 
(?pf2 != rdf:type ) && 
(?pf2 != skos:subject ) && 
(?pf2 != <http://dbpedia.org/property/wikiPageUsesTemplate> ) && 
(?pf2 != <http://dbpedia.org/property/wordnet_type> ) && 
(?ps1 != rdf:type ) && 
(?ps1 != skos:subject ) && 
(?ps1 != <http://dbpedia.org/property/wikiPageUsesTemplate> ) && 
(?ps1 != <http://dbpedia.org/property/wordnet_type> ) && 
(!isLiteral(?middle)) && 
(?middle != <http://dbpedia.org/resource/Rome> ) && 
(?middle != <http://dbpedia.org/resource/Lazio> ) && 
(?middle != ?of1 ) && 
(!isLiteral(?of1)) && 
(?of1 != <http://dbpedia.org/resource/Rome> ) && 
(?of1 != <http://dbpedia.org/resource/Lazio> ) && 
(?of1 != ?middle )
). 
} LIMIT 10
"""

print urllib2.quote(s)



