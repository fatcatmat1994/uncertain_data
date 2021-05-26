from pointBase import PointSet
from dataLoader import DataSet

class Permutation(object):
    def __init__(self, pSt: PointSet, order: dict):
        self.pSt = pSt
        # self.order = {"loc": Point_Object}
        self.SV = 0
        self.order = order
        self.__iter_num = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_num += 1
        if self.__iter_num >= len(self.pSt):
            self.__iter_num = -1
            raise StopIteration
        return self.order[self.__iter_num]

    def __len__(self):
        return len(self.pSt)

    def get_pSt(self):
        return self.pSt

    def get_order(self):
        return self.order

class SampleResult(object):
    def __init__(self):
        self.__member = []
        self.__iter_num = -1

    def __iter__(self):
        return self

    def __getitem__(self, item):
        return self.__member[item]

    def __next__(self):
        self.__iter_num += 1
        if self.__iter_num >= len(self.__member):
            self.__iter_num = -1
            raise StopIteration
        return self.__member[self.__iter_num]

    def __len__(self):
        return len(self.__member)

    def add_member(self, member: Permutation):
        self.__member.append(member)



class Sampler(object):
    def __init__(self, sample_num: int, threshold: float):
        self.sample_num = sample_num
        self.sample_result = []
        self.threshold = threshold

    # 待实现
    def sample(self, dataSet: DataSet)->SampleResult:
        self.data = dataSet
        sample_res = SampleResult()
        for p_lab in dataSet.get_labs().values():
            p_lab.sort()


        return SampleResult()