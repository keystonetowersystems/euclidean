import unittest

from euclidean.R2.line import Line, P2

class LineTestCase(unittest.TestCase):

    def test_create_from_points(self):

        l = Line.ByPoints(P2(-1, -1), P2(1, 1))

        self.assertEqual(l.y(1), 1)
        self.assertEqual(l.y(-1), -1)
        self.assertEqual(l.x(1), 1)
        self.assertEqual(l.x(-1), -1)

        self.assertEqual(l.y(25), 25)
        self.assertEqual(l.y(-25), -25)
        self.assertEqual(l.x(25), 25)
        self.assertEqual(l.x(-25), -25)

        l = Line.ByPoints(P2(-1, 1), P2(1, -1))

        self.assertEqual(l.y(1), -1)
        self.assertEqual(l.y(-1), 1)
        self.assertEqual(l.x(1), -1)
        self.assertEqual(l.x(-1), 1)

        self.assertEqual(l.y(25), -25)
        self.assertEqual(l.y(-25), 25)
        self.assertEqual(l.x(25), -25)
        self.assertEqual(l.x(-25), 25)

    def test_degenerate_cases(self):

        vert = Line.ByPoints(P2(1, 1), P2(1, -1))

        self.assertEqual(vert.y(1), None)
        self.assertEqual(vert.y(-100), None)
        self.assertEqual(vert.x(-1), 1)
        self.assertEqual(vert.x(1), 1)
        self.assertEqual(vert.x(-100), 1)
        self.assertEqual(vert.x(100), 1)

        horz = Line.ByPoints(P2(-1, 0), P2(1, 0))

        self.assertEqual(horz.y(-1), 0)
        self.assertEqual(horz.y(1), 0)
        self.assertEqual(horz.y(-100), 0)
        self.assertEqual(horz.y(100), 0)

        self.assertEqual(horz.x(-1), None)
        self.assertEqual(horz.x(1), None)
        self.assertEqual(horz.x(-100), None)
        self.assertEqual(horz.x(100), None)

    def test_intersection(self):

        horz = Line.ByPoints(P2(-1, 10), P2(1, 10))
        vert = Line.ByPoints(P2(10, -1), P2(10, 1))

        self.assertEqual(horz.intersection(vert), P2(10, 10))

        self.assertEqual(horz.intersection(horz), None)
        self.assertEqual(horz.intersection(Line.ByPoints(P2(-1, 0), P2(1, 0))), None)

        l45 = Line.ByPoints(P2(0, 0), P2(1,1))
        self.assertEqual(horz.intersection(l45), P2(10, 10))

        l135 = Line.ByPoints(P2(0, 0), P2(-1, 1))
        self.assertEqual(horz.intersection(l135), P2(-10, 10))

    def test_closest_point(self):
        horz = Line.ByPoints(P2(-1, 10), P2(1, 10))

        self.assertEqual(horz.closest(P2(0, 0)), P2(0, 10))
        self.assertEqual(horz.closest(P2(5, 10)), P2(5, 10))

        vert = Line.ByPoints(P2(10, 1), P2(10, -2))

        self.assertEqual(vert.closest(P2(0, 5)), P2(10, 5))
        self.assertEqual(vert.closest(P2(10, 5)), P2(10, 5))


