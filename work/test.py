from hmm import HMM_Model
import re

def set_model():
    model = HMM_Model()
    with open('./data/training_data.txt', mode='r', encoding='utf-8') as f:
        training_data = f.read()           
    training_data = eval(training_data) 
    model.train(training_data)
    return model

def get_data():
    data = ""
    with open('./data/test_data.txt', mode='r', encoding='utf-8') as f:
        data = f.read()    
    sentences = re.split('[，。？！；：「」]', data)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip()
        if sentences[i] == "":
            sentences.pop(i)
    return sentences

def process(model,sentences):
    for s in sentences:
        print()
        print("-------------------------------------")
        print("(" + s + ")")        
        ans_list = model.predict_sentence(s)
        for s_str, s_tag in ans_list:
            if s_tag != "O" and s_tag[0] == "B":
                print()
                print(s_tag[2:], end=" ")
                print(s_str, end='')
            elif s_tag != "O":
                print(s_str, end='')
    
if __name__ == '__main__':
    model = set_model()
    sentences = get_data()
    print()
    process(model,sentences)
    
    