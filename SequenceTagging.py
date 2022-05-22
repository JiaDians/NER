import json
import re
source = 'TVBS新聞網'
data_type = '全球'
sentences = []
lines = []
with open('C.txt', 'r', encoding='UTF-8') as f1:
    lines = f1.readlines()
    
print('Total article count:', len(lines))
for j in range(len(lines)): # article count
    print('article:', str(j+1))
    result = json.loads(lines[j].replace("\'", "\""))
    print('Total Filtered Sentences:', len(result['Filtered Sentences']))
    # Tagging
    sentences = result['Filtered Sentences']
    SentenceTag = []
    for i in range(len(sentences)):
        print('-------------------------------------')
        print('sentence', str(i+1))
        print(sentences[i])

        need = input("(y/n):")
        while need != "y" and need != "n":
            need = input("(y/n):")
        
        # set up data4_dict
        data4_dict = dict()
        data4_dict['source'] = source
        data4_dict['type'] = data_type
        data4_dict['date'] = result['date']
        data4_dict['text'] = sentences[i]
        data4_dict['tag'] = ['' for s in sentences[i]]
        if need == "n":
            continue
        elif need == "y":
            print('[P/L/O/D/T] + & + [str] or "g"')
            instruction = input()
            while not(len(instruction) == 1 and instruction == "g"):
                if len(instruction.split('&')) == 2:
                    instruction_list = instruction.split('&')
                    if sentences[i].find(instruction_list[1]) == -1:
                        print('string not found')
                    else:
                        if instruction_list[0].upper() == 'P':
                            for match in re.finditer(instruction_list[1], sentences[i]):
                                pos = match.start()
                                IsFirstUse = False
                                for index in range(pos, pos + len(instruction_list[1])):
                                    if data4_dict['tag'][index] == "":
                                        if IsFirstUse == False:
                                            data4_dict['tag'][index] = 'B-PER'
                                            # Insert U-PER
                                            if (index-1) >= 0:
                                                if data4_dict['tag'][index-1] == "":
                                                    data4_dict['tag'][index-1] = 'U-PER'
                                            IsFirstUse = True
                                        else:
                                            data4_dict['tag'][index] = 'I-PER'
                                # Insert D-PER
                                if pos + len(instruction_list[1]) < len(sentences[i]):
                                    if data4_dict['tag'][pos + len(instruction_list[1])] == "":
                                        data4_dict['tag'][pos + len(instruction_list[1])] = 'D-PER'
                        elif instruction_list[0].upper() == 'L':         
                            for match in re.finditer(instruction_list[1], sentences[i]):
                                pos = match.start()
                                IsFirstUse = False
                                for index in range(pos, pos + len(instruction_list[1])):
                                    if data4_dict['tag'][index] == "":
                                        if IsFirstUse == False:
                                            data4_dict['tag'][index] = 'B-LOC'
                                            # Insert U-LOC
                                            if (index-1) >= 0:
                                                if data4_dict['tag'][index-1] == "":
                                                    data4_dict['tag'][index-1] = 'U-LOC'
                                            IsFirstUse = True
                                        else:
                                            data4_dict['tag'][index] = 'I-LOC'
                                # Insert D-LOC
                                if pos + len(instruction_list[1]) < len(sentences[i]):
                                    if data4_dict['tag'][pos + len(instruction_list[1])] == "":
                                        data4_dict['tag'][pos + len(instruction_list[1])] = 'D-LOC'
                        elif instruction_list[0].upper() == 'O':    
                            for match in re.finditer(instruction_list[1], sentences[i]):
                                pos = match.start()
                                IsFirstUse = False
                                for index in range(pos, pos + len(instruction_list[1])):
                                    if data4_dict['tag'][index] == "":
                                        if IsFirstUse == False:
                                            data4_dict['tag'][index] = 'B-ORG'
                                            # Insert U-ORG
                                            if (index-1) >= 0:
                                                if data4_dict['tag'][index-1] == "":
                                                    data4_dict['tag'][index-1] = 'U-ORG'
                                            IsFirstUse = True
                                        else:
                                            data4_dict['tag'][index] = 'I-ORG'
                                # Insert D-ORG
                                if pos + len(instruction_list[1]) < len(sentences[i]):
                                    if data4_dict['tag'][pos + len(instruction_list[1])] == "":
                                        data4_dict['tag'][pos + len(instruction_list[1])] = 'D-ORG'
                        elif instruction_list[0].upper() == 'D':     
                            for match in re.finditer(instruction_list[1], sentences[i]):
                                pos = match.start()
                                IsFirstUse = False
                                for index in range(pos, pos + len(instruction_list[1])):
                                    if data4_dict['tag'][index] == "":
                                        if IsFirstUse == False:
                                            data4_dict['tag'][index] = 'B-Date'
                                            IsFirstUse = True
                                        else:
                                            data4_dict['tag'][index] = 'I-Date'
                        elif instruction_list[0].upper() == 'T':
                            for match in re.finditer(instruction_list[1], sentences[i]):
                                pos = match.start()
                                IsFirstUse = False
                                for index in range(pos, pos + len(instruction_list[1])):
                                    if data4_dict['tag'][index] == "":
                                        if IsFirstUse == False:
                                            data4_dict['tag'][index] = 'B-Time'
                                            IsFirstUse = True
                                        else:
                                            data4_dict['tag'][index] = 'I-Time'
                        else:
                            pass
                else:
                    print('wrong format')
                print('[P/L/O/D/T] + & + [str] or "g"')
                instruction = input()
            
            # Insert O
            for index in range(len(data4_dict['tag'])):
                if data4_dict['tag'][index] == '':
                    data4_dict['tag'][index] = 'O'
            
            # write to D.txt
            
            with open('D.txt', 'a') as fa:
                fa.write(str(data4_dict) + '\n')
            
    # Continue new article work?
    IsWork = input("Continue new article work? (y/n):")
    while IsWork != "y" and IsWork != "n":
        IsWork = input("(y/n):")
    if IsWork == 'y':
        print('-------------------------------------')
    else:
        with open('C.txt', 'w') as fw:
            for line in lines[j+1:]:
                fw.write(str(line) + '\n')
        print('Update C.txt succeeded.')
        break

                
            
                