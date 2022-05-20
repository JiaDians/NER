import re
import json

KeywordsList = []
with open('./data/LastName.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        for word in line.rstrip('\n').split(','):
            KeywordsList.append(word)
with open('./data/PlaceName.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        for word in line.rstrip('\n').split(','):
            KeywordsList.append(word)
with open('./data/OrganizationName.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        for word in line.rstrip('\n').split(','):
            KeywordsList.append(word)

with open('A.txt', 'r') as fr:
    lines = fr.readlines()
    with open('B.txt', 'w') as fw:
        for i in range(len(lines)): # article count
            print('article:', str(i+1))
            result = json.loads(lines[i].replace("\'", "\""))
            sentences = re.split('[，。？！]', result['article'])
            
            ImportantSentences = []
            for sentence in sentences:
                for Keywords in KeywordsList:
                    if Keywords in sentence:
                        ImportantSentences.append(sentence)
                        break
            data2_dict = dict()
            data2_dict['date'] = result['date']
            data2_dict['Unfiltered Sentences'] = ImportantSentences
            fw.write(str(data2_dict) + '\n')
        