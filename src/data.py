from itertools import combinations
import numpy as np

class DataGenerator(object):

    def __init__(self, lab_num: int, prob_num: int):
        self.lab_num = lab_num
        self.prob_num = prob_num
        self.VS = {}
        self.labs = list(map(
            str, range(int)
        ))
        self.prob = {}


    def __generator_prob(self):
        """
            "prob": {
                "A_0": 0.5,
                "A_1": 0.5,
                "B_0": 0.3,
                "B_1": 0.7
            }
        :param self:
        :return:
        """
        for lab in self.labs:
            prob = np.random.randint(1, 10, size = (1, self.prob_num))
            for i in range(self.prob_num):
                lab_str = lab + "_" + str(i)



        pass