from src.dataLoader import DataSet
from src.utils import load_json


def main():
    f_pth = "data/test.json"
    data = load_json(f_pth)
    # data = {"prob": prob, "vs": vs, "points": points}
    prob, vs, points = data["prob"], data["vs"], data["points"]
    data_set = DataSet(points, prob, vs)



if __name__ == '__main__':
    print_hi('PyCharm')

