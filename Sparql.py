from copy import copy
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import os
import nltk
from nltk.corpus import treebank
import spacy
from spacy import displacy
from nltk import Tree
#import pudb
from nltk import Tree
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
spacy.load('en')


data_id = []
question = []
keywords = []
query = []
dataset = []

porter_stemmer = PorterStemmer()
stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than' ,'this' ,'where'] 

def entity_recogniser ( text ) :
	text_spotlight = copy(text)
	text_spotlight = text_spotlight.replace(" ","%20").replace(",","%2C").replace("?","%3F")

	r = os.popen('curl -sX GET "https://api.dbpedia-spotlight.org/en/spot?text='+text_spotlight+'" -H  "accept: application/json"').read()
	try:
	  r = json.loads(r)['annotation']['surfaceForm']
	  if type(r) is dict:
	  	r = [r]
	except:
	  r = []

	spotlight_ners=[]
	spotlight_ners_capitalised=[]
	spotlight_ners_hyphenated=[]

	for each in r:
		text_here = each['@name']
		spotlight_ners.append(text_here)
		spotlight_ners_capitalised.append(text_here[0].upper()+text_here[1:])
		spotlight_ners_hyphenated.append((text_here[0].upper()+text_here[1:]).replace(" ","_"))


	print("spotlight ners: "+str(spotlight_ners_hyphenated))

	text_pn = copy(text)

	for i in range(len(spotlight_ners)):
		text_pn = text_pn.replace(spotlight_ners[i], spotlight_ners_hyphenated[i])

	# print("pn_before: "+str(text_pn))
	text_pn_org = copy(text_pn)

	text_pn = text_pn.split()

	entities_org = []
	entities = []
	entity = ""
	entity_now = ""
	entity_found = False
	between = 0

	for i in range(len(text_pn)):
		if i == 0:
			continue
		if text_pn[i][0].isupper():
			entity_found = True
			entity_now+=text_pn[i]+" "
			if i == len(text_pn) - 1:
				entity = entity_now
				entities.append(entity.strip().replace(" ","_"))
				entities_org.append(entity.strip())
		else:
			if (text_pn[i] == "at" or text_pn[i] == "is" or text_pn[i] == "in" or text_pn[i] == "of") and entity_found:
				entity_now+=text_pn[i]+" "
			else:
				entity = entity_now.strip()
				entity_found = False
				if entity!="":
					entities.append(entity.replace(" ","_"))
					entities_org.append(entity)
					entity_now=""
				entity = ""

	print("Entities finally: "+str(entities))
	# print(entities_org)

	for i in range(len(entities)):
		entity_org = entities_org[i]
		entity = entities[i]

		text_pn_org = text_pn_org.replace(entity_org, entity)

	print("Hyphenated queries: " + text_pn_org)

	return ( entities , text_pn_org )



def predicate_recogniser( query,entities ):
	query = query.strip(",")
	query = query.strip("?")
	query = query.strip(".")
	query = query.strip(":")
	query = query.strip(";")
	query = query.strip()
	tokens = word_tokenize(query) 
	  
	filtered_tokens = [w for w in tokens if not w.lower() in stop_words] 
	  
	# filtered_tokens = [] 
	  
	# for w in tokens: 
	#     if w not in stop_words: 
	#         filtered_tokens.append(w) 
	  

	print("filtered predicates: "+str(filtered_tokens)) 

	entities_l = [w.lower() for w in entities]
	#print("l "+str(entities_l))
	
	raw_predicates= []
	for w in filtered_tokens:
		if w.lower() not in entities_l:
			raw_predicates.append(w)
	print("raw predicates "+str(raw_predicates))
	stemmed_predicates = []

	for w in raw_predicates:
		stemmed_predicates.append(porter_stemmer.stem(w))

	print(stemmed_predicates)
	return stemmed_predicates, raw_predicates


def getdata():
    input_file = open('LargeDataset.json','r')
    json_decode=json.load(input_file)
    data = json_decode['questions']
    for item in data:
        data_id.append(item['id'])
        question.append(item['question'][0]['string'])
        keywords.append(item['question'][0]['keywords'])
        query.append(item['query']['sparql'])



getdata()




text = input("Enter text: ")
print("\n")
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)

# sub_toks = [tok for tok in doc if(tok.dep_ == "nsubj")]
# print("sub_toks:" + str(sub_toks))

boolean_query=["Does","Did","Is","Was"]
query_type=0

if(doc[0].text in boolean_query):
	query_type=1

entities , hyphenated_text = entity_recogniser(text)
print("\n")

text = text.strip()
text = text.strip(",")
text = text.strip("?")
text = text.strip(".")
text = text.strip(":")
text = text.strip(";")
text = text.strip()

print("\n")
entities , hyphenated_text = entity_recogniser(text)

doc = nlp(hyphenated_text)

subject = [tok for tok in doc if(tok.dep_ == "nsubj")]
print("\nsubject:" + str(subject) + "\n")

stemmed_predicates,refined_predicates = predicate_recogniser(hyphenated_text, entities)

sparql_query="PREFIX dbo: <http://dbpedia.org/ontology/>\nPREFIX res: <http://dbpedia.org/resource/>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"


print("POS Tagging: ")
pos_list = []
for token in doc:
    pos_list.append((token.text, token.pos_, token.tag_, spacy.explain(token.tag_)))
print(pos_list)


print("\n")
if(query_type):
	sparql_query = sparql_query + "ASK\nWHERE{\n"
else:
	sparql_query = sparql_query + "SELECT DISTINCT ?a\nWHERE{\n"

sub_flag=0
subj=""
if(len(subject)):
	for i in pos_list:
		if(subject[0].text==i[0] and ((i[2]=='NNP') or (i[2]=='NNS') or (i[2]=='NN'))):
			sub_flag=1
			subj=i[0]


obj=""
pred=""
keywords_gen=refined_predicates+entities
if(sub_flag):
	if(subj!=""):
		if(len(keywords_gen)==3):
			for i in pos_list:
				if((i[0] in keywords_gen) and (i[1]=='VERB')):
					pred=i[0]
			for i in keywords_gen:
				if(i!=pred and i!=subj):
					obj=i
			sparql_query = sparql_query + "\tres:"+subj+"\tdbo:"+pred+"\t?x .\n"
			sparql_query = sparql_query + "\t?x\trdf:type\tres:"+obj+" .\n"
		elif(len(keywords_gen)==2):
			for i in keywords_gen:
				if(i!=subj):
					pred=i
			sparql_query = sparql_query + "\tres:"+subj+"\tdbo:"+pred+"\t?a .\n"
	else:
		print("HI")

else:
	if(len(keywords_gen)==2):
		if(len(entities)==1):
			obj=entities[0]
		else:
			for i in pos_list:
				if((i[0] in entities) and (i[2]=='NNP' or i[2]=='NNS' or i[2]=='NN')):
					obj=i[0]
					break
		for i in keywords_gen:
			if(i != obj):
				pred=i
		sparql_query = sparql_query + "\t?a\tdbo:"+pred+"\tres:"+obj+".\n"
	if(len(keywords_gen)==3):
		print("HI")


sparql_query = sparql_query + "}"
print(sparql_query)