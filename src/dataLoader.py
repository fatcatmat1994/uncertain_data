from pointBase import Point, PointSet, PointLabels
import json

class DataSet(object):
    def __init__(self, master_labs: list, prob: dict, vs: dict):
        self.__pSt = PointSet()
        self.__OLabs = master_labs
        self.__OProb = prob
        self.__OVs = vs
        self.__NLabs = {lab: PointLabels(master_label = lab) for lab in master_labs}
        self.__NVs = {PointSet() : 0} # 空集
        self.length = len(points)

        # 这两个为了保持不同地方引用的对象一致
        self.__S2Pst = {} # String to PointSet-Object
        self.__S2P = {} # String to Point-Object
        self.__transform()

    def __len__(self):
        return self.length

    def __trans_lab(self):
        '''
        转化labels和概率
        :return:
        e.g.
            self.prob = {
                "A_0": 0.5,
                "A_1": 0.5,
                "B_0": 0.3,
                "B_1": 0.7
            }
        '''
        for lab_str, prob in self.__OProb.items():
            lab_str = lab_str.strip()
            tmp_l = lab_str.split("_")
            lab, p_no = tmp_l[0].strip(), int(tmp_l[1].strip())
            # 设置HashMap
            # Point对象只在此调用并产生
            p = self.__S2P.setdefault(lab_str, Point(label = lab, no = p_no, prob = prob))

            pSt = self.__S2Pst.setdefault(lab_str, PointSet())
            pSt.add_point(p)
            self.__pSt.add_point(p)
            self.__S2P[lab_str] = p
            # 设置Labels
            self.__NLabs[lab].add_point(p)

    def __trans_values(self):
        """
        :return:
        e.g.
            vs = {
                "A_0": 1,
                "A_1": 2,
                "B_0": 3,
                "B_1": 4,
                "A_0,B_0": 5,
                "A_0, B_1" :  6,
                "A_1,B_0": 6,
                "A_1, B_1": 9
            }
        """
        for lab_str_c, value in self.__OVs.items():
            lab_str_c = lab_str_c.strip()
            lab_l = lab_str_c.split(',')
            if len(lab_l) == 1:
                lab_str = lab_l[0].strip()
                pSt = self.__S2Pst[lab_str]
            else:
                pSt = PointSet()
                for lab_str in lab_l:
                    lab_str = lab_str.strip()
                    pSt.add_point(self.__S2P[lab_str])
            self.__S2Pst[lab_str_c] = pSt
            self.__NVs[pSt] = value

    def __transform(self):
        self.__trans_lab()
        self.__trans_values()

    def get_S2Pst(self):
        return self.__S2Pst

    def get_S2P(self):
        return self.__S2P

    def get_pSt(self):
        return self.__pSt

    def get_labs(self):
        return self.__NLabs

    def get_values(self):
        return self.__NVs



def read_json(file_path):
    with open(file_path, 'w') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    points = ["A", "B"]

    prob = {
        "A_0": 0.5,
        "A_1": 0.5,
        "B_0": 0.3,
        "B_1": 0.7
    }
    vs = {
        "A_0": 1,
        "A_1": 2,
        "B_0": 3,
        "B_1": 4,
        "A_0,B_0": 5,
        "A_0, B_1" :  6,
        "A_1,B_0": 6,
        "A_1, B_1": 9
    }

    data = {"prob": prob, "vs": vs, "points": points}
    with open("../data/test.json", "w") as f:
        json.dump(data, f)

    dt = DataSet(points, prob, vs)
    print("S2P: ", dt.get_S2P())
    print("S2Pst", dt.get_S2Pst())
    print("POINT_SET: ", dt.get_pSt())
    print("VALUES: ", dt.get_values())
    print("LABELS: ", dt.get_labs())

    d = dt.get_values()
    print(d is dt.get_values())
    SV = {p.label: 0.0 for p in dt.get_pSt()}
    print(SV)
