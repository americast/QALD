from SPARQLWrapper import SPARQLWrapper, JSON

entities = ["Unfinished_Portrait_of_general_Bonaparte"]
entities = [each.replace("_"," ") for each in entities]
# print(entities)

sparql = SPARQLWrapper("http://10.35.32.94:9999/blazegraph/namespace/DBpedia/sparql")
sparql.setQuery("""
	prefix bds: <http://www.bigdata.com/rdf/search#>
	select ?s ?p ?o ?score ?rank
	where {
	?o bds:search "Unfinished Portrait of general Bonaparte" .
	?o bds:matchAllTerms "true" .
	?o bds:minRelevance "0.25" .
	?o bds:relevance ?score .
	?o bds:maxRank "1000" .
	?o bds:rank ?rank .
	?s ?p ?o .
	}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results['results']['bindings'][0]['s']['value'])