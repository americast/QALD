from copy import copy
import json
import os


text = input("Enter text: ")

text_spotlight = copy(text)
text_spotlight = text_spotlight.replace(" ","%20").replace(",","%2C").replace("?","%3F")

r = os.popen('curl -sX GET "https://api.dbpedia-spotlight.org/en/spot?text='+text_spotlight+'" -H  "accept: application/json"').read()
try:
  r = json.loads(r)['annotation']['surfaceForm']
  if type(r) is dict:
  	r = [r]
except:
  r = []
# print(r)

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

print(text_pn_org)

# for entity in entities:
# 	ind = text.find(entity)
# 	text_here = text[ind:]
# 	num_words = len(text.split())
# 	for i in range(num_words):
