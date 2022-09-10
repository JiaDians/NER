import numpy as np
from tqdm import tqdm
import random

# BIO - M
class HMM_Model_BIO:
    def __init__(self):
        self.tag2id = {'B-PER': 0,
                       'I-PER': 1,
                       'B-LOC': 2,
                       'I-LOC': 3,
                       'B-ORG': 4,
                       'I-ORG': 5,
                       'B-DATE': 6,
                       'I-DATE': 7,
                       'B-TIME': 8,
                       'I-TIME': 9,
                       'O': 10}
        
        self.id2tag = dict(zip(self.tag2id.values(), self.tag2id.keys()))
        self.num_tag = len(self.tag2id)
        self.num_char = 65536
        self.A = np.zeros((self.num_tag, self.num_tag))
        self.B = np.zeros((self.num_tag, self.num_char))
        self.pi = np.zeros(self.num_tag)
        self.epsilon = 1e-100
        
    def train(self, data): 
        print('training...')
        progress = tqdm(total=len(data))
        for i in range(len(data)):
            for j in range(len(data[i][0])):
                cut_char = data[i][0][j]
                cut_tag = data[i][1][j]
                self.B[self.tag2id[cut_tag]][ord(cut_char)] += 1
                if j == 0:
                    self.pi[self.tag2id[cut_tag]] += 1
                else:
                    # pre_char = training_data[i][0][j-1]
                    pre_tag = data[i][1][j-1]
                    self.A[self.tag2id[pre_tag]][self.tag2id[cut_tag]] += 1
            progress.update(1)

       
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        
    def viterbi(self, Obs):
        T = len(Obs)
        delta = np.zeros((T, self.num_tag))
        psi = np.zeros((T, self.num_tag))
        
        delta[0] = self.pi[:] + self.B[:, ord(Obs[0])]
        for i in range(1, T):    
            temp = delta[i - 1].reshape(self.num_tag, -1) + self.A
            delta[i] = np.max(temp, axis=0)
            delta[i] = delta[i, :] + self.B[:, ord(Obs[i])]
            psi[i] = np.argmax(temp, axis=0)

        # print(psi)
        path = np.zeros(T)
        path[T - 1] = np.argmax(delta[T - 1])
        for i in range(T - 2, -1, -1):
            path[i] = int(psi[i + 1][int(path[i + 1])])
        return path

    def predict_sentence(self, Obs_s):
        T = len(Obs_s)
        path = self.viterbi(Obs_s)
        ans_list = []
        for i in range(T):
            ans_list.append([Obs_s[i],self.id2tag[path[i]]])
            # print(ans_list[i][0], ans_list[i][1])
        return ans_list
    
    def predict_list(self,Obs_l):
        word_total = 0
        correct_count = 0
        Obs_s = ""
        path_list = []
        for i in range(len(Obs_l)):
            word_total += len(Obs_l[i][0])
            Obs_s = Obs_l[i][0]
            T = len(Obs_s)
            path = self.viterbi(Obs_s)
            path_list.append([Obs_s,[self.id2tag[tid] for tid in path]])
            for j in range(T):
                # print(self.id2tag[path[j]], Obs_l[i][1][j])
                if self.id2tag[path[j]] == Obs_l[i][1][j]:
                    correct_count += 1
        return round(correct_count / word_total * 100, 1), path_list
        
# BIO - S - PER
class HMM_Model_BIO_PER:
    def __init__(self):
        self.tag2id = {'B-PER': 0,
                       'I-PER': 1,
                       'O': 2}
        
        self.id2tag = dict(zip(self.tag2id.values(), self.tag2id.keys()))
        self.num_tag = len(self.tag2id)
        self.num_char = 65536
        self.A = np.zeros((self.num_tag, self.num_tag))
        self.B = np.zeros((self.num_tag, self.num_char))
        self.pi = np.zeros(self.num_tag)
        self.epsilon = 1e-100
        
    def train(self, data): 
        print('training...')
        progress = tqdm(total=len(data))
        for i in range(len(data)):
            for j in range(len(data[i][0])):
                cut_char = data[i][0][j]
                cut_tag = data[i][1][j]
                self.B[self.tag2id[cut_tag]][ord(cut_char)] += 1
                if j == 0:
                    self.pi[self.tag2id[cut_tag]] += 1
                else:
                    # pre_char = training_data[i][0][j-1]
                    pre_tag = data[i][1][j-1]
                    self.A[self.tag2id[pre_tag]][self.tag2id[cut_tag]] += 1
            progress.update(1)

       
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        
    def viterbi(self, Obs):
        T = len(Obs)
        delta = np.zeros((T, self.num_tag))
        psi = np.zeros((T, self.num_tag))
        
        delta[0] = self.pi[:] + self.B[:, ord(Obs[0])]
        for i in range(1, T):    
            temp = delta[i - 1].reshape(self.num_tag, -1) + self.A
            delta[i] = np.max(temp, axis=0)
            delta[i] = delta[i, :] + self.B[:, ord(Obs[i])]
            psi[i] = np.argmax(temp, axis=0)

        # print(psi)
        path = np.zeros(T)
        path[T - 1] = np.argmax(delta[T - 1])
        for i in range(T - 2, -1, -1):
            path[i] = int(psi[i + 1][int(path[i + 1])])
        return path

    def predict_sentence(self, Obs_s):
        T = len(Obs_s)
        path = self.viterbi(Obs_s)
        ans_list = []
        for i in range(T):
            ans_list.append([Obs_s[i],self.id2tag[path[i]]])
            # print(ans_list[i][0], ans_list[i][1])
        return ans_list
    
    def predict_list(self,Obs_l):
        word_total = 0
        correct_count = 0
        Obs_s = ""
        path_list = []
        for i in range(len(Obs_l)):
            word_total += len(Obs_l[i][0])
            Obs_s = Obs_l[i][0]
            T = len(Obs_s)
            path = self.viterbi(Obs_s)
            path_list.append([Obs_s,[self.id2tag[tid] for tid in path]])
            for j in range(T):
                # print(self.id2tag[path[j]], Obs_l[i][1][j])
                if self.id2tag[path[j]] == Obs_l[i][1][j]:
                    correct_count += 1
        return round(correct_count / word_total * 100, 1), path_list
        
# BIO - S - ORG
class HMM_Model_BIO_ORG:
    def __init__(self):
        self.tag2id = {'B-ORG': 0,
                       'I-ORG': 1,
                       'O': 2}
        
        self.id2tag = dict(zip(self.tag2id.values(), self.tag2id.keys()))
        self.num_tag = len(self.tag2id)
        self.num_char = 65536
        self.A = np.zeros((self.num_tag, self.num_tag))
        self.B = np.zeros((self.num_tag, self.num_char))
        self.pi = np.zeros(self.num_tag)
        self.epsilon = 1e-100
        
    def train(self, data): 
        print('training...')
        progress = tqdm(total=len(data))
        for i in range(len(data)):
            for j in range(len(data[i][0])):
                cut_char = data[i][0][j]
                cut_tag = data[i][1][j]
                self.B[self.tag2id[cut_tag]][ord(cut_char)] += 1
                if j == 0:
                    self.pi[self.tag2id[cut_tag]] += 1
                else:
                    # pre_char = training_data[i][0][j-1]
                    pre_tag = data[i][1][j-1]
                    self.A[self.tag2id[pre_tag]][self.tag2id[cut_tag]] += 1
            progress.update(1)

       
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        
    def viterbi(self, Obs):
        T = len(Obs)
        delta = np.zeros((T, self.num_tag))
        psi = np.zeros((T, self.num_tag))
        
        delta[0] = self.pi[:] + self.B[:, ord(Obs[0])]
        for i in range(1, T):    
            temp = delta[i - 1].reshape(self.num_tag, -1) + self.A
            delta[i] = np.max(temp, axis=0)
            delta[i] = delta[i, :] + self.B[:, ord(Obs[i])]
            psi[i] = np.argmax(temp, axis=0)

        # print(psi)
        path = np.zeros(T)
        path[T - 1] = np.argmax(delta[T - 1])
        for i in range(T - 2, -1, -1):
            path[i] = int(psi[i + 1][int(path[i + 1])])
        return path

    def predict_sentence(self, Obs_s):
        T = len(Obs_s)
        path = self.viterbi(Obs_s)
        ans_list = []
        for i in range(T):
            ans_list.append([Obs_s[i],self.id2tag[path[i]]])
            # print(ans_list[i][0], ans_list[i][1])
        return ans_list
    
    def predict_list(self,Obs_l):
        word_total = 0
        correct_count = 0
        Obs_s = ""
        path_list = []
        for i in range(len(Obs_l)):
            word_total += len(Obs_l[i][0])
            Obs_s = Obs_l[i][0]
            T = len(Obs_s)
            path = self.viterbi(Obs_s)
            path_list.append([Obs_s,[self.id2tag[tid] for tid in path]])
            for j in range(T):
                # print(self.id2tag[path[j]], Obs_l[i][1][j])
                if self.id2tag[path[j]] == Obs_l[i][1][j]:
                    correct_count += 1
        return round(correct_count / word_total * 100, 1), path_list
        
# BIO - S - LOC
class HMM_Model_BIO_LOC:
    def __init__(self):
        self.tag2id = {'B-LOC': 0,
                       'I-LOC': 1,
                       'O': 2}
        
        self.id2tag = dict(zip(self.tag2id.values(), self.tag2id.keys()))
        self.num_tag = len(self.tag2id)
        self.num_char = 65536
        self.A = np.zeros((self.num_tag, self.num_tag))
        self.B = np.zeros((self.num_tag, self.num_char))
        self.pi = np.zeros(self.num_tag)
        self.epsilon = 1e-100
        
    def train(self, data): 
        print('training...')
        progress = tqdm(total=len(data))
        for i in range(len(data)):
            for j in range(len(data[i][0])):
                cut_char = data[i][0][j]
                cut_tag = data[i][1][j]
                self.B[self.tag2id[cut_tag]][ord(cut_char)] += 1
                if j == 0:
                    self.pi[self.tag2id[cut_tag]] += 1
                else:
                    # pre_char = training_data[i][0][j-1]
                    pre_tag = data[i][1][j-1]
                    self.A[self.tag2id[pre_tag]][self.tag2id[cut_tag]] += 1
            progress.update(1)

       
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        
    def viterbi(self, Obs):
        T = len(Obs)
        delta = np.zeros((T, self.num_tag))
        psi = np.zeros((T, self.num_tag))
        
        delta[0] = self.pi[:] + self.B[:, ord(Obs[0])]
        for i in range(1, T):    
            temp = delta[i - 1].reshape(self.num_tag, -1) + self.A
            delta[i] = np.max(temp, axis=0)
            delta[i] = delta[i, :] + self.B[:, ord(Obs[i])]
            psi[i] = np.argmax(temp, axis=0)

        # print(psi)
        path = np.zeros(T)
        path[T - 1] = np.argmax(delta[T - 1])
        for i in range(T - 2, -1, -1):
            path[i] = int(psi[i + 1][int(path[i + 1])])
        return path

    def predict_sentence(self, Obs_s):
        T = len(Obs_s)
        path = self.viterbi(Obs_s)
        ans_list = []
        for i in range(T):
            ans_list.append([Obs_s[i],self.id2tag[path[i]]])
            # print(ans_list[i][0], ans_list[i][1])
        return ans_list
    
    def predict_list(self,Obs_l):
        word_total = 0
        correct_count = 0
        Obs_s = ""
        path_list = []
        for i in range(len(Obs_l)):
            word_total += len(Obs_l[i][0])
            Obs_s = Obs_l[i][0]
            T = len(Obs_s)
            path = self.viterbi(Obs_s)
            path_list.append([Obs_s,[self.id2tag[tid] for tid in path]])
            for j in range(T):
                # print(self.id2tag[path[j]], Obs_l[i][1][j])
                if self.id2tag[path[j]] == Obs_l[i][1][j]:
                    correct_count += 1
        return round(correct_count / word_total * 100, 1), path_list
        

def main():
    model = HMM_Model_BIO_LOC()
    with open('./data/training_data.txt', mode='r', encoding='utf-8') as f:
        data = f.read()           
    data = eval(data)  
    # data = [["str",[tag]],["str",[tag]]...,["str",[tag]]]
    
    # 分割 train data (80%) / test data (20%)
    pos_list = list([i for i in range(len(data))])
    random.shuffle(pos_list) 
    # 設定訓練資料
    train_data = []
    for i in range(len(data) * 80 // 100):
        train_data.append(data[pos_list[i]])
    # 設定測試資料
    test_data = []
    for i in range((len(data) * 80) // 100, len(data)):
        test_data.append(data[pos_list[i]])
    # 開始訓練
    model.train(train_data)
    
    # 預測
    accuracy, path_list = model.predict_list(test_data)
    print()
    print("Accuracy =", accuracy, "%")
    s = '黃婦於11日下午9時21分往杉林大橋'
    ans_list = model.predict_sentence(s)

    return ans_list, path_list

if __name__ == '__main__':
    ans_list, path_list = main()
