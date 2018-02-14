import unittest
from utils import Rectangle, SpatialRelation


class RectangleTests(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(Rectangle(1, 2, 3, 4), Rectangle(1, 2, 3, 4))
        self.assertNotEqual(Rectangle(10, 2, 3, 4), Rectangle(1, 2, 3, 4))
        self.assertNotEqual(Rectangle(1, 20, 3, 4), Rectangle(1, 2, 3, 4))
        self.assertNotEqual(Rectangle(1, 2, 30, 4), Rectangle(1, 2, 3, 4))
        self.assertNotEqual(Rectangle(1, 2, 3, 40), Rectangle(1, 2, 3, 4))

    def test_area(self):
        a = Rectangle(2, 3, 3, 5)
        self.assertEqual(a.area(), 15)

    def test_xmax_ymax(self):
        a = Rectangle(2, 3, 3, 5)
        self.assertEqual(a.xmax, 5)
        self.assertEqual(a.ymax, 8)

    def test_intersect(self):
        a = Rectangle(1, 3, 3, 7)
        b = Rectangle(2, 1, 3, 6)
        c = Rectangle(5, 3, 3, 6)
        d = Rectangle(5, 0, 3, 2)

        self.assertEqual(a.signed_intersect(b), Rectangle(2, 3, 2, 4), 'overlapping')
        self.assertEqual(b.signed_intersect(a), Rectangle(2, 3, 2, 4), 'overlapping reverse')
        self.assertEqual(a.signed_intersect(a), a, 'equal')
        self.assertEqual(a.signed_intersect(c), Rectangle(5, 3, -1, 6), 'no intersect, x negative')
        self.assertEqual(a.signed_intersect(d), Rectangle(5, 3, -1, -1), 'no intersect, x amd y negative')

    def test_union(self):
        a = Rectangle(1, 3, 3, 7)
        b = Rectangle(2, 1, 3, 6)
        self.assertEqual(a.union(b), Rectangle(1, 1, 4, 9), 'overlapping')
        self.assertEqual(b.union(a), Rectangle(1, 1, 4, 9), 'overlapping reverse')
        self.assertEqual(a.union(a), a, 'equal')


class RelationTests(unittest.TestCase):
    def test_EQ(self):
        a = Rectangle(1, 1, 2, 4)
        b = Rectangle(1, 1, 2, 4)
        r = SpatialRelation(a, b)
        self.assertTrue(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_DC(self):
        a = Rectangle(1, 1, 2, 4)
        b = Rectangle(3.01, 0, 8, 0.2)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertTrue(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_EC(self):
        a = Rectangle(1, 1, 2, 5)
        b = Rectangle(3, 0, 8, 2)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertTrue(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_PO(self):
        a = Rectangle(1, 1, 2, 4)
        b = Rectangle(2, 2, 3.5, 1)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertTrue(r.PO(), "PO")

    def test_TPP(self):
        a = Rectangle(2, 2, 1, 1)
        b = Rectangle(1, 1, 2, 4)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertTrue(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_TPPi(self):
        b = Rectangle(2, 2, 1, 1)
        a = Rectangle(1, 1, 2, 4)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertTrue(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_NTPP(self):
        a = Rectangle(2, 2, 1, 1)
        b = Rectangle(1, 1, 2.1, 4)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertTrue(r.NTPP(), "NTPP")
        self.assertFalse(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")

    def test_NTPPi(self):
        b = Rectangle(2, 2, 1, 1)
        a = Rectangle(1, 1, 2.1, 4)
        r = SpatialRelation(a, b)
        self.assertFalse(r.EQ(), "EQ")
        self.assertFalse(r.DC(), "DC")
        self.assertFalse(r.EC(), "EC")
        self.assertFalse(r.TPP(), "TPP")
        self.assertFalse(r.TPPi(), "TPPi")
        self.assertFalse(r.NTPP(), "NTPP")
        self.assertTrue(r.NTPPi(), "NTPPi")
        self.assertFalse(r.PO(), "PO")



if __name__ == '__main__':
    unittest.main()
