import unittest

from euclidean.R2.space import P2
from euclidean.R2.polygon.polygon import Polygon

from euclidean.R2.polygon.hull import _jarvis_convex_hull

class PolygonTest(unittest.TestCase):

    def setUp(self):
        self.ccw_polygon = Polygon([
            P2(0, 0),
            P2(1, 0),
            P2(1, 1),
            P2(0, 1)
        ])

        self.cw_polygon = Polygon([
            P2(0, 0),
            P2(0, 1),
            P2(1, 1),
            P2(1, 0)
        ])

        self.ccw_intersecting = Polygon([
            P2(0, 0),
            P2(1, 1),
            P2(0, 1),
            P2(1, 0)
        ])

        self.cw_intersecting = Polygon([
            P2(0, 0),
            P2(1, 1),
            P2(1, 0),
            P2(0, 1)
        ])

    def test_simple(self):
        self.assertTrue(self.ccw_polygon.is_simple())
        self.assertTrue(self.cw_polygon.is_simple())

    def test_intersecting(self):
        self.assertFalse(self.ccw_intersecting.is_simple())
        self.assertFalse(self.cw_intersecting.is_simple())

    def test_ccw_polygon_contains(self):

        self.assertTrue(P2(0.5, 0.5) in self.ccw_polygon)
        self.assertFalse(P2(2, 2) in self.ccw_polygon)
        self.assertFalse(P2(-1, -1) in self.ccw_polygon)

    def test_cw_polygon_contains(self):

        self.assertTrue(P2(0.5, 0.5) in self.cw_polygon)
        self.assertFalse(P2(2,2) in self.cw_polygon)
        self.assertFalse(P2(-1, -1) in self.cw_polygon)

    def test_ccw_polygon_centroid(self):
        self.assertEqual(self.ccw_polygon.centroid(), P2(0.5, 0.5))

    def test_cw_polygon_centroid(self):
        self.assertEqual(self.cw_polygon.centroid(), P2(0.5, 0.5))

    def test_cw_area(self):
        self.assertEqual(self.cw_polygon.area(), 1)

    def test_ccw_area(self):
        self.assertEqual(self.ccw_polygon.area(), 1)

    def test_jarvis_convex_hull(self):
        points = [
            P2(0, 3),
            P2(2, 2),
            P2(1, 1),
            P2(2, 1),
            P2(3, 0),
            P2(0, 0),
            P2(3, 3)
        ]
        points = sorted(points, key=lambda p: p._coords)
        expected = [P2(0, 0), P2(3, 0), P2(3, 3), P2(0, 3)]
        for a, e in zip(_jarvis_convex_hull(points), expected):
            self.assertEqual(a, e)