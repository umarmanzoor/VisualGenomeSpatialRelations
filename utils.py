from pathlib import Path

data_dir = Path('data/')
rels_path = data_dir / 'relationships.json'
objects_path = data_dir / 'objects.json'
image_data_path = data_dir / 'image_data.json'


class Rectangle:
    def __init__(self, x, y, w, h):
        self.xmin = x
        self.ymin = y
        self.w = w
        self.h = h
        self.xmax = x + w
        self.ymax = y + h

    def __str__(self):
        return '[%d, %d, %d, %d]' % (self.xmin, self.ymin, self.w, self.h)

    def __eq__(self, other):
        return self.xmin == other.xmin and self.ymin == other.ymin and \
               self.w == other.w and self.h == other.h

    def signed_intersect(self, other):
        r = Rectangle(max(self.xmin, other.xmin), max(self.ymin, other.ymin),
                      min(self.xmax, other.xmax), min(self.ymax, other.ymax))
        if r.xmin <= r.xmax and r.ymin <= r.ymax:
            return r
        return Rectangle(0, 0, -1, -1)

    def union(self, other):
        r = Rectangle(min(self.xmin, other.xmin), min(self.ymin, other.ymin),
                      max(self.xmax, other.xmax), max(self.ymax, other.ymax))
        return r

    def area(self):
        return 0 if self.h <= 0 or self.w <= 0 else self.w * self.h


class SpatialRelation:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.intersect = a.signed_intersect(b)
        self.union = a.union(b)
        self.x_intersect = self.intersect.w / self.union.w
        self.y_intersect = self.intersect.h / self.union.h
        self.__threshold = 0.1

    # a equals to b
    def EQ(self):
        return self.a == self.b

    # a inside b and touching
    def TPP(self):
        return not self.EQ() and \
               self.intersect == self.a and \
               self.x_intersect <= self.__threshold and \
               self.y_intersect <= self.__threshold

    # b inside a and touching
    def TPPi(self):
        return not self.EQ() and \
               self.intersect == self.b and \
               self.x_intersect <= self.__threshold and \
               self.y_intersect <= self.__threshold

    # a inside b and not touching
    def NTPP(self):
        return not self.EQ() and \
               self.intersect == self.a and \
               not self.TPP()

    # b inside a and not touching
    def NTPPi(self):
        return not self.EQ() and \
               self.intersect == self.b and \
               not self.TPPi()

    # a and b are far from each other
    def DC(self):
        # x distance or y distance is bigger than threshold
        return self.x_intersect < -1 * self.__threshold or \
               self.y_intersect < -1 * self.__threshold

    # a and b are not inside each other and x_distance and y_distance between them is within the threshold
    def EC(self):
        return not self.DC() and \
               self.intersect != self.a and \
               self.intersect != self.b and \
               self.x_intersect <= self.__threshold and \
               self.y_intersect <= self.__threshold

    # a and b overlapping but none of them inside the other
    def PO(self):
        return not self.DC() and \
               not self.EC() and \
               self.intersect != self.a and \
               self.intersect != self.b
