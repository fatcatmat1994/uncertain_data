from math import log, exp
from random import choice, Random

class Point(object):
    def __init__(self, label: str, no: int, prob: float):
        self.label = label
        self.no = no
        self.prob = prob
        self.SV = 0
        self.__describe = self.label + '_' + str(self.no) + "@" + str(self.prob)

    def get_desc(self):
        return self.__describe

    def __repr__(self):
        return f"Point({self.__describe})"

    def __hash__(self):
        return hash(self.__describe)

    def __eq__(self, other):
        return self.label == other.label and self.no == other.no

    def __lt__(self, other):
        return self.prob < other.prob

class PointSet(object):
    def __init__(self):
        self.__pSt = set()
        self.__describe = "Empty Set"
        self.__prob = 0

    def __len__(self):
        return len(self.__pSt)

    def __repr__(self):
        return f"PointSet({self.__describe})"

    def __hash__(self):
        return hash(self.__describe)

    def __eq__(self, other):
        return self.__pSt == other.__pSt

    def __iter__(self):
        return iter(self.__pSt)

    def __update(self):
        self.__describe = ",".join([p.get_desc() for p in self.__pSt])

    def get_desc(self):
        return self.__describe

    def get_pSt(self):
        return self.__pSt

    def get_prob(self):
        return exp(self.__prob)

    def add_point(self, p: Point):
        self.__pSt.add(p)
        self.__prob += log(p.prob)
        self.__update()

    def differ(self, other):
        c = self.__pSt.union(other.__pointSet)
        diff = self.__pSt - c
        return create_pSt_from_set(diff)

def create_pSt_from_set(s: set)->PointSet:
    pSt = PointSet()
    for p in s:
        pSt.add_point(p)
    return pSt

class PointLabels(object):
    def __init__(self, master_label: str):
        '''
        该类定义了标签的结构 例如A {1, 2, 3}
        :param label: 标签类型 例如A
        '''
        self.__master_label = master_label
        self.__SV = 0
        self.__members = []
        self.__iter_num = -1

    def __repr__(self):
        return f"PointLabels({self.__master_label}@{list(range(len(self.__members)))})"

    def __len__(self):
        return len(self.__members)

    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_num += 1
        if self.__iter_num >= len(self.__members):
            self.__iter_num = -1
            raise StopIteration
        return self.__members[self.__iter_num]

    def __update_SV(self):
        self.__SV = sum([p.SV * p.prob for p in self.__members])

    def get_lab(self):
        return self.__master_label

    def get_SV(self):
        self.__update_SV()
        return self.__SV

    def get_member(self):
        return self.__members

    def add_point(self, p: Point):
        self.__members.append(p)

    def sort(self):
        self.__members.sort(reverse = True)

    def random_choice(self, random_choice: Random)->Point:
        return random_choice.choice(self.__members)

if __name__ == '__main__':
    p = PointSet()
    p.add_point(Point("A", 0, 0.3))
    p.add_point(Point("A", 1, 0.7))
    d = {p : 1}
    a = PointSet()
    a.add_point(Point("A", 0, 0.3))
    a.add_point(Point("A", 1, 0.7))
    print(p == a)
    print(d[a])
    for t in iter(p):
        print(t)
    for t in iter(p):
        print(t)