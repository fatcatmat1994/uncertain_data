from pointBase import PointSet


class BucketMember(object):
    def __init__(self, member: PointSet, master: PointSet, diffNum: int, diff_set: PointSet):
        self.member = member
        self.master = master
        self.diffNum = diffNum
        self.diff_set = diff_set


class Bucket(object):
    def __init__(self, master: PointSet):
        self.master = master
        self.members = set([])
        self.num = 0

    def add_member(self, per: PointSet):
        # 计算相似度 以及与主元素的差别
        diff_set = self.master.differ(per)
        diffNum = len(diff_set)
        b_mem = BucketMember(per, self.master, diffNum, diff_set)
        self.members.add(b_mem)
        self.num += 1


class BucketSet(object):
    def __init__(self):
        self.__buckets = {}
        self.max_diffNum = 0

    def __getitem__(self, item):
        return self.__buckets[item]

    def add_bucket(self, bucket: Bucket):
        self.max_diffNum += 1
        self.__buckets[self.max_diffNum] = bucket
        print("Success Add bucket")

    def items(self):
        return self.__buckets.items()

def setBucket(per: PointSet, bucket_set: BucketSet):
    flag = False
    for diffNum, bucket in bucket_set.items():
        bucket_master = bucket.master
        diff = bucket_master.differ(per)
        if diffNum == len(diff):
            bucket.add_member(per)
            flag = True
            break

    if not flag:
        new_bucket = Bucket(master=per)
        bucket_set.add_bucket(new_bucket)
