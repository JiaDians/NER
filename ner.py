from hmm import HMM_Model
import re


def set_model():
    model = HMM_Model()
    with open('./data/training_data.txt', mode='r', encoding='utf-8') as f:
        training_data = f.read()
    training_data = eval(training_data)
    model.train(training_data)
    return model


def get_data(data):
    sentences = re.split('[，。？！；：「」]', data)
    index = 0
    while index < len(sentences):
        sentences[index] = sentences[index].strip()
        if sentences[index] == "":
            sentences.pop(index)
            continue
        index += 1
    return sentences


def process(model, sentences):
    entity_list = []
    for i in range(len(sentences)):
        entity_list.append([[], []])
        entity_list[i][0] = sentences[i]
        ans_list = model.predict_sentence(sentences[i])
        count = -1
        for s_str, s_tag in ans_list:
            if s_tag != "O" and s_tag[0] == "B":
                entity_list[i][1].append([[], ""])
                count += 1
                entity_list[i][1][count][0] = s_tag[2:]
                entity_list[i][1][count][1] += s_str
            elif s_tag != "O":
                entity_list[i][1][count][1] += s_str
    return entity_list


def get_entity(data):
    model = set_model()
    sentences = get_data(data)
    entity_list = process(model, sentences)
    return entity_list


if __name__ == '__main__':
    model = set_model()
    data = ""
    with open('./data/test_data.txt', mode='r', encoding='utf-8') as f:
        data = f.read()
    sentences = get_data(data)
    entity_list = process(model, sentences)
