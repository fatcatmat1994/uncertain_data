from pointBase import PointSet, Point
from dataLoader import DataSet
from random import Random
from error import MyError
from utils import load_json
from math import log, exp
from loserTree import LoserTree


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

    def add_member(self, member):
        self.__members.append(member)

class Sampler(object):
    def __init__(self, max_iter: int, threshold: float,  K: int, seed = None):
        self.__max_iter = max_iter
        self.__seed = 0 if seed is None else seed
        self.__Random = Random(self.__seed)
        self.__log_threshold = log(threshold)
        self.__K = K

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

    def __copy(self, pSt: PointSet):
        new_pSt = PointSet()
        for p in pSt:
            new_pSt.add_point(p)
        return new_pSt

    # 待实现
    def prob_sample(self, data_set: DataSet)->SampleResult:
        K = data_set.PROB_WORLD if data_set.PROB_WORLD < self.__K else self.__K

        sample_res = SampleResult()
        labs = data_set.get_labs()
        labs_l = list(labs.values())

        add_pSt = PointSet()
        max_prob, now_prob, min_prob = 0, 0, 0


        for lab in labs_l:
            lab.sort()
            now_prob += log(lab[0].prob)
            max_prob += log(lab[0].prob)
            min_prob += log(lab[-1].prob)
        sample_res.add_member(add_pSt)

        ptr = [0] * data_set.length
        ls_tree = LoserTree(labs_l)

        # if self.__log_threshold < min_prob or self.__log_threshold > max_prob:
        #     raise MyError(f"给予的阈值有错误， 应在 {exp(min_prob)} ~ {exp(max_prob)} 之间")

        now_iter = 0
        while(len(sample_res) < K and now_iter < self.__max_iter):
            now_iter += 1
            add_pSt = self.__copy(add_pSt)
            # 最小值的索引
            loser_idx = ls_tree.get_loser_idx()
            # 最小值所在的labs集合
            loser_lab = labs[loser_idx]
            loser_p = loser_lab[ptr[loser_idx]]
            add_pSt.remove_point(loser_p)

            # ptr[loser_idx]为下一个Point
            ptr[loser_idx] += 1

            # 更新结点并调整败者树
            while(ptr[loser_idx] == len(loser_lab)):
                # 计算第二小的数
                ls_tree.update_data(loser_idx, 2.0)
                tmp_loser_idx = ls_tree.get_loser_idx()
                tmp_loser_p = loser_lab[ptr[tmp_loser_idx]]
                add_pSt.remove_point(tmp_loser_p)

                # 把第一小的点的第一个label重新加回去
                ptr[loser_idx] = 0
                add_pSt.add_point(loser_lab[0])
                ls_tree.update_data(loser_idx, loser_lab[0].prob)

                # 重新计算败者
                ptr[tmp_loser_idx] += 1

                loser_idx = ls_tree.get_loser_idx()
                loser_lab = labs[loser_idx]

            add_p = loser_lab[ptr[loser_idx]]

            add_pSt.add_point(add_p)
            sample_res.add_member(add_pSt)
        return sample_res

if __name__ == '__main__':
    f_pth = "../data/test.json"
    data = load_json(f_pth)
    # data = {"prob": prob, "vs": vs, "points": points}
    prob, vs, points = data["prob"], data["vs"], data["points"]
    dt = DataSet(points, prob, vs)
    sampler = Sampler(2, 0.7)
    sampler.prob_sample(dt)

    tmp_pSt, add_pSt = PointSet(), PointSet()
    add_pSt.add_point(Point("A", 0, 1))
    d = {1: add_pSt}
    add_pSt = PointSet()
    print(add_pSt)
    print(d)
