import json
with open(r'../C.txt', 'r') as f:
    lines = f.readlines()

with open('./test/test_data.txt', 'w', encoding='UTF-8') as f1:
    test_list = []
    for i in range(len(lines)):
        result = json.loads(lines[i].replace("\'", "\""))
        temp_list = []
        temp_list.append(result['text'])
        temp_list.append(result['tag'])
        test_list.append(temp_list)
    f1.write(str(test_list))
    with open('../C.txt', 'w', encoding='UTF-8') as f2:
        f2.flush()

    