import json
import nltk
from nltk.corpus import treebank
import spacy
from spacy import displacy
spacy.load('en')


data_id = []
question = []
keywords = []
query = []
dataset = []

def getdata():
	input_file = open('data/LargeDataset.json','r')
	json_decode=json.load(input_file)
	data = json_decode['questions']
	for item in data:
		data_id.append(item['id'])
		question.append(item['question'][0]['string'])
		keywords.append(item['question'][0]['keywords'])
		query.append(item['query']['sparql'])
	

# sentence = "Did Tony Fry influence Aristotle?"
# sentence1 = "Does Por tu amor have more episodes than Game of Thrones?"
# sentence2 = "Give me all books written by David Foster Wallace."


# print("########### NLTK #############")

# tokens = nltk.word_tokenize(sentence)

# tagged = nltk.pos_tag(tokens)
# print(tagged)

# entities = nltk.chunk.ne_chunk(tagged)
# print(entities)

# keywords = []
# for items in tagged:
# 	if(items[1] == "NNP" or items[1] == "NNS" or items[1] == "NNPS" or items[1] == "NN" ):
# 		keywords.append(items)
# print("Keywords: " + str(keywords))

getdata()
		

print("########### SPACY #############")

length = len(data_id)

nlp = spacy.load('en_core_web_sm')

for i in range(5,10):
	print("\n\n")
	print(data_id[i])
	print(question[i])

	doc = nlp(question[i])

	print("POS Tagging: ")
	pos_list = []
	for token in doc:
	    pos_list.append((token.text, token.pos_, token.tag_, spacy.explain(token.tag_)))
	print(pos_list)

	print("\nNamed Entity Recognition: ")
	ner_list = []
	for ent in doc.ents:
		ner_list.append((ent.text, ent.label_))
	print(ner_list)

	print("\nTokens to take: ")
	notToTake = ['VBZ','VBD','VBP','IN','DT','.','PRP']
	toTake = []
	for token in doc:
		if(token.tag_ not in notToTake):
			toTake.append(token)
	print(toTake)
