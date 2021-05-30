from dataLoader import DataSet
from copy import deepcopy

MAX = 1 << 31
MIN = -MAX

class LoserTree:
    def __init__(self, labs_l: list):
        self.__labs_l = labs_l
        self.__N = len(labs_l)
        self.__ls = [self.__N] * self.__N
        self.__probArray = [labs[0].prob for labs in labs_l]
        self.__probArray.append(MIN)
        self.__build_tree()



    def __adjust(self, idx: int):
        pIdx = (idx + self.__N) // 2
        while(pIdx > 0):
            if self.__probArray[idx] > self.__probArray[self.__ls[pIdx]]:
                self.__probArray[pIdx], idx = idx, self.__probArray[pIdx]
            pIdx = pIdx // 2
        self.__ls[0] = idx


    def __build_tree(self):
        for i in range(self.__N):
            self.__adjust(i)

    def get_loser_idx(self):
        return self.__ls[0]

    def update_data(self, idx: int, prob: float):
        self.__probArray[idx] = prob
        self.__adjust(idx)




