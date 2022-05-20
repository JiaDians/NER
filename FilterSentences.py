import json

lines = []
with open('B.txt', 'r') as f1:
    lines = f1.readlines()
    
print('Total article count:', len(lines))
for i in range(len(lines)): # article count
    print('article:', str(i+1))
    result = json.loads(lines[i].replace("\'", "\""))
    print('Total Unfiltered Sentences:', len(result['Unfiltered Sentences']))
    # filter
    sentences = result['Unfiltered Sentences']
    FilteredSentences = []
    for i in range(len(sentences)):
        print('-------------------------------------')
        print('sentence', str(i+1))
        print(sentences[i])

        need = input("(y/m/n):")
        
        while need != "y" and need != "m" and need != "n":
            need = input("(y/m/n):")
        if need == "y":
            FilteredSentences.append(sentences[i])
        elif need == "m":
            filter_s = input("filtered content:")
            FilteredSentences.append(filter_s.strip())
 
    # write to C.txt
    data3_dict = dict()
    data3_dict['date'] = result['date']
    data3_dict['FilteredSentences'] = FilteredSentences
    with open('C.txt', 'a') as fa:
        fa.write(str(data3_dict) + '\n')
        
    # Continue new article work?
    IsWork = input("Continue new article work? (y/n):")
    while IsWork != "y" and IsWork != "n":
        IsWork = input("(y/n):")
    if IsWork == 'n':
        with open('B.txt', 'w') as fw:
            for line in lines[i+1:]:
                fw.write(str(line) + '\n')
        break
            
                
            
                