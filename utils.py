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

    def __repr__(self):
        return 'rect' + self.__str__()

    def __eq__(self, other):
        return self.xmin == other.xmin and self.ymin == other.ymin and \
               self.w == other.w and self.h == other.h

    def signed_intersect(self, other):
        xmin = max(self.xmin, other.xmin)
        ymin = max(self.ymin, other.ymin)
        xmax = min(self.xmax, other.xmax)
        ymax = min(self.ymax, other.ymax)
        return Rectangle(xmin, ymin, xmax - xmin, ymax - ymin)

    def union(self, other):
        xmin = min(self.xmin, other.xmin)
        ymin = min(self.ymin, other.ymin)
        xmax = max(self.xmax, other.xmax)
        ymax = max(self.ymax, other.ymax)
        return Rectangle(xmin, ymin, xmax - xmin, ymax - ymin)

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

    # a equals to b
    def EQ(self):
        return self.a == self.b

    def touching_inside(self):
        if self.intersect != self.a and self.intersect != self.b:  # not inside
            return False
        return \
            abs(self.a.xmin - self.b.xmin) == 0 or \
            abs(self.a.xmax - self.b.xmax) == 0 or \
            abs(self.a.ymin - self.b.ymin) == 0 or \
            abs(self.a.ymax - self.b.ymax) == 0

    # a inside b and touching
    def TPP(self):
        return not self.EQ() and \
               self.intersect == self.a and \
               self.touching_inside()

    # b inside a and touching
    def TPPi(self):
        return not self.EQ() and \
               self.intersect == self.b and \
               self.touching_inside()

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
        return self.x_intersect < 0 or \
               self.y_intersect < 0

    def EC(self):
        return self.x_intersect == 0 or self.y_intersect == 0

    # a and b overlapping but none of them inside the other
    def PO(self):
        return self.intersect.area() > 0 and \
               self.intersect != self.a and \
               self.intersect != self.b
