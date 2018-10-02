from copy import copy

text = input("Enter text: ")
text_org = copy(text)
text = text.split()

entities_org = []
entities = []
entity = ""
entity_now = ""
entity_found = False
between = 0

for i in range(len(text)):
	if i == 0:
		continue
	if text[i][0].isupper():
		entity_found = True
		entity_now+=text[i]+" "
		if i == len(text) - 1:
			entity = entity_now
			entities.append(entity.strip().replace(" ","-"))
			entities_org.append(entity.strip())
	else:
		if (text[i] == "at" or text[i] == "is" or text[i] == "in" or text[i] == "of") and entity_found:
			entity_now+=text[i]+" "
		else:
			entity = entity_now.strip()
			entity_found = False
			if entity!="":
				entities.append(entity.replace(" ","-"))
				entities_org.append(entity)
				entity_now=""
			entity = ""

print(entities)
print(entities_org)

for i in range(len(entities)):
	entity_org = entities_org[i]
	entity = entities[i]

	text_org = text_org.replace(entity_org, entity)

print(text_org)

# for entity in entities:
# 	ind = text.find(entity)
# 	text_here = text[ind:]
# 	num_words = len(text.split())
# 	for i in range(num_words):
