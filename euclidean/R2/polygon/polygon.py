import numpy as np
import operator

from itertools import chain
from collections import deque

from euclidean.constants import tau
from euclidean.R2.space import P2, V2
from euclidean.R2.line import LineSegment

from .hull import convex_hull
from .line_sweep import shamos_hoey

class Polygon:

    @classmethod
    def ConvexHull(cls, points):
        return cls(convex_hull(points))

    def __init__(self, points):
        self._points = tuple(points)
        assert(len(self._points) >= 3)

    def _rolled(self, offset):
        return chain(self._points[offset:], self._points[:offset])

    def _cross_products(self):
        return map(V2.cross, self._points, self._rolled(1))

    def area(self):
        """Find the area of this polygon.

        Notes:

            This will return an incorrect value if the polygon is complex.

        Returns:

        """
        return 0.5 * abs(sum(self._cross_products()))

    def centroid(self):
        """Find the centroid of this polygon.

        Notes:

            This will return an incorrect value if the polygon is complex.

        Returns:

        """
        cx, cy, a = 0, 0, 0
        for p1, p2 in zip(self._points, self._rolled(1)):
            cross = V2.cross(p1, p2)
            cx += (p1.x + p2.x) * cross
            cy += (p1.y + p2.y) * cross
            a += cross
        a *= 3
        return P2(cx / a, cy / a)

    def translate(self, vector):
        return Polygon(p + vector for p in self._points)

    def center(self, new_center_point):
        """Copy this polygon centered at the provided point.

        Returns:
            (Polygon):
        """
        vector = new_center_point - self.centroid()
        return Polygon(p - vector for p in self._points)

    def rotate(self, radians, center_point=None):
        """Rotate the polygon by radians around a center point or the centroid if none is provided.

        Args:
            radians:
            center_point:

        Returns:
            (Polygon)
        """
        center_point = center_point if center_point else self.centroid()
        return Polygon(p.rotate(radians, center_point) for p in self._points)

    def points(self):
        return self._points

    def xs(self):
        return (p.x for p in self._points)

    def ys(self):
        return (p.y for p in self._points)

    def is_convex(self):
        #todo:
        pass

    def is_simple(self):
        return shamos_hoey(self.edges())

    def edges(self):
        return map(LineSegment, self._points, chain(self._points[1:], self._points[:1]))

    def __contains__(self, test_point):
        return self.winding_number(test_point) > 0

    def perimeter(self):
        return sum(edge.length() for edge in self.edges())

    def winding_number(self, test_point):
        order = sum(self._cross_products())
        wn = 0
        for edge in self.edges():
            if edge._p1.y <= test_point.y:
                if edge._p2.y > test_point.y:
                    if order * P2.CCW(edge._p1, edge._p2, test_point) > 0:
                        wn += 1
            else:
                if edge._p2.y <= test_point.y:
                    if order * P2.CCW(edge._p1, edge._p2, test_point) < 0:
                        wn -= 1
        return wn

