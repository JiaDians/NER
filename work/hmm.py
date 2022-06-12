import numpy as np
from tqdm import tqdm

class HMM_Model:
    def __init__(self):
        self.tag2id = {'B-PER': 0,
                       'I-PER': 1,
                       'U-PER': 2,
                       'D-PER': 3,
                       'B-LOC': 4,
                       'I-LOC': 5,
                       'U-LOC': 6,
                       'D-LOC': 7,
                       'B-ORG': 8,
                       'I-ORG': 9,
                       'U-ORG': 10,
                       'D-ORG': 11,
                       'B-DATE': 12,
                       'I-DATE': 13,
                       'B-TIME': 14,
                       'I-TIME': 15,
                       'O': 16}
        
        self.id2tag = dict(zip(self.tag2id.values(), self.tag2id.keys()))
        self.num_tag = len(self.tag2id)
        self.num_char = 65536
        self.A = np.zeros((self.num_tag, self.num_tag))
        self.B = np.zeros((self.num_tag, self.num_char))
        self.pi = np.zeros(self.num_tag)
        self.epsilon = 1e-100

    def train(self, corpus_path):
        with open(corpus_path, mode='r', encoding='utf-8') as f:
            training_data = f.read()           
        training_data = eval(training_data)   
        
        print('training...')
        progress = tqdm(total=len(training_data))
        for i in range(len(training_data)):
            for j in range(len(training_data[i][0])):
                cut_char = training_data[i][0][j]
                cut_tag = training_data[i][1][j]
                self.B[self.tag2id[cut_tag]][ord(cut_char)] += 1
                if j == 0:
                    self.pi[self.tag2id[cut_tag]] += 1
                else:
                    # pre_char = training_data[i][0][j-1]
                    pre_tag = training_data[i][1][j-1]
                    self.A[self.tag2id[pre_tag]][self.tag2id[cut_tag]] += 1
            progress.update(1)
        
        
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        print('finish')

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

        print(psi)
        path = np.zeros(T)
        path[T - 1] = np.argmax(delta[T - 1])
        for i in range(T - 2, -1, -1):
            path[i] = int(psi[i + 1][int(path[i + 1])])
        return path

    def predict(self, Obs):
        T = len(Obs)
        path = self.viterbi(Obs)
        for i in range(T):
            print(Obs[i], self.id2tag[path[i]])


def main():
    model = HMM_Model()
    model.train('./training/training_data.txt')
    s = '黃婦於11日下午9時21分沿高129線往杉林大橋方向步行'
    model.predict(s)

if __name__ == '__main__':
    main()
