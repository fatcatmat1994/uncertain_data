from scipy.special import comb
from dataLoader import DataSet
from sample import Sampler, Permutation
from pointBase import PointSet


class ShapleyValue(object):
    def __init__(self, data:DataSet, sample_num: int, threshold: float, max_iter: int):
        self.data = data
        self.sampler = Sampler(sample_num, threshold)
        # self.sample_result : SampleResult
        self.sample_result = self.sampler.perm_sample(self.data)
        self.N = len(self.data)
        self.max_iter = max_iter
        self.VS = self.data.get_values()
        self.SV = {p.label:0 for p in self.data.get_pSt()}


    def __computes(self, v1: float, v2: float, S_length: int) -> float:
        return 1 / (self.N * comb(self.N - 1, S_length)) * (v2 - v1)

    def __shapley(self, permutation: Permutation):
        prob = permutation.get_pSt().get_prob()
        L_pSt = PointSet()
        v1, S_length = 0, 0
        for p in permutation:
            v1 = self.VS[L_pSt]
            L_pSt.add_point(p)
            v2 = self.VS[L_pSt]

            # update

            S_length += 1

    def pShapleyValue(self):
        for perm in self.sample_result:
            self.__shapley(perm)
