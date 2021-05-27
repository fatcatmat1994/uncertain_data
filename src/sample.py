from pointBase import PointSet, Point
from dataLoader import DataSet
from random import Random
from error import MyError

class Permutation(object):
    def __init__(self):
        self.__pSt = PointSet()
        # self.order = {"loc": Point_Object}
        self.__prob = 1
        self.__SV = {}
        self.__order = {}
        self.__iter_num = -1
        self.__HashMap = {}

    def add_point(self, p: Point, loc: int):
        if self.__order.get(loc, None) is None:
            self.__order[loc] = p
        else:
            raise MyError(f"位置{loc}上已经有点{p.label}_{p.no}")

        if self.__HashMap.get(p.label, False) == False:
            self.__HashMap[p.label] = True
            self.__pSt.add_point(p)
            self.__prob *= p.prob
        else:
            raise MyError(f"重复插入标签 {p.label}")

    def get_pSt(self):
        return self.__pSt

    def get_prob(self):
        return self.__prob

    def get_order(self):
        return self.__order

    def update_SV(self, lab_str, SV):
        self.__SV[lab_str] = SV


    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_num += 1
        if self.__iter_num >= len(self.__pSt):
            self.__iter_num = -1
            raise StopIteration
        return self.__order[self.__iter_num]

    def __len__(self):
        return len(self.__pSt)


class SampleResult(object):
    def __init__(self):
        self.__members = []
        self.__iter_num = -1

    def __iter__(self):
        return self

    def __getitem__(self, item):
        return self.__members[item]

    def __next__(self):
        self.__iter_num += 1
        if self.__iter_num >= len(self.__members):
            self.__iter_num = -1
            raise StopIteration
        return self.__members[self.__iter_num]

    def __len__(self):
        return len(self.__members)

    def add_member(self, member: Permutation):
        self.__members.append(member)





class Sampler(object):
    def __init__(self, max_iter: int, threshold: float, seed = None):
        self.__max_iter = max_iter
        self.__threshold = threshold
        self.__seed = 0 if seed is None else seed
        self.__Random = Random(self.__seed)

    def __get_random_permutation(self, data_set: DataSet) -> Permutation:
        labs = data_set.get_labs()
        lab_str_l = list(data_set.get_labs().keys())
        self.__Random.shuffle(lab_str_l)
        perm = Permutation()
        for loc, lab_str in enumerate(lab_str_l):
            p = labs[lab_str].random_choice(self.__Random)
            perm.add_point(p = p, loc = loc)
        return perm

    def perm_sample(self, data_set: DataSet)->SampleResult:
        self.data = data_set
        sample_res = SampleResult()
        now_iter = 0
        while(now_iter < self.__max_iter):
            now_iter += 1
            sample_res.add_member(self.__get_random_permutation(data_set))
        return sample_res

    # 待实现
    def prob_sample(self, data_set: DataSet)->SampleResult:
        sample_res = SampleResult()



        return sample_res
