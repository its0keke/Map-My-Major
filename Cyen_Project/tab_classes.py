import sys

def importFile():
    file = open(sys.argv[1], "r")
    entities = []
    for entity in file:
      entities.append(entity.rstrip())
    file.close()

    return entities

def calcTabs(line):
	tabs = 0
	for i in range(len(line)):
		if line[i] == '\t':
			tabs += 1
		else:
			return tabs

entities = importFile()
print entities
print calcTabs(entities[2])

# classes = {}
# for i in range(len(entities)):
#     tabs = calcTabs(entities[i])
#     prereqs = []
#     for j in range(i, len(entities)):
#         if calcTabs(entities[j]) == tabs:
#             prereqs.append(entities[j])
#         else:
#             classes[entities[j]] = prereqs
#         print prereqs
#
# print classes
