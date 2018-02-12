import numpy as np
import matplotlib.pyplot as plt

from typing import Callable, Iterable

#from collections.abc import Iterable

from .vector import Vector3, Vector2
from .shapes2 import PolyLine2,PolyLineSet2

class TruncatedCone:

    def __init__(self, base_diameter, top_diameter, height):
        assert(base_diameter >= top_diameter)
        assert(height > 0)
        self.base_diameter = base_diameter
        self.top_diameter = top_diameter
        self.height = height

    def diameter_difference(self):
        return self.base_diameter - self.top_diameter

    def radius_difference(self):
        return self.diameter_difference() / 2

    def slope(self):
        return self.diameter_difference() / (2 * self.height)

    def slant_height(self):
        return np.sqrt(self.radius_difference() ** 2 + self.height ** 2)

    def peak(self):
        return self.base_diameter / self.diameter_difference() * self.height

class PolyLine3:

    __slots__ = ['_xs', '_ys', '_zs']

    def __init__(self, points : Iterable[Vector3] = None, dtype=np.float64):
        self.set(points, dtype)

    def set(self, points : Iterable[Vector3] = None, dtype=np.float64):
        if points:
            unzipper = ((p.x, p.y, p.z) for p in points)
            (xs, ys, zs) = zip(*unzipper)
        else:
            (xs, ys, zs) = ([], [], [])

        self._xs = np.array(xs, dtype=dtype)
        self._ys = np.array(ys, dtype=dtype)
        self._zs = np.array(zs, dtype=dtype)
        return self

    def points_raw(self):
        return zip(self._xs, self._ys, self._zs)

    def points(self):
        return (Vector3(x, y, z) for (x, y, z) in self.points_raw())

    def filter(self, predicate : Callable[[Vector3], bool]):
        indices = [predicate(v3) for v3 in self.points()]
        filtered = PolyLine3()
        filtered._xs = self._xs[indices]
        filtered._ys = self._ys[indices]
        filtered._zs = self._zs[indices]
        return filtered


    def concat(self, polyline):
        assert(isinstance(polyline, PolyLine3))
        return self.append_raw(polyline._xs, polyline._ys, polyline._zs)

    def append_raw(self, xs, ys, zs):
        self._xs = np.append(self._xs, xs)
        self._ys = np.append(self._ys, ys)
        self._zs = np.append(self._zs, zs)
        return self

    def append(self, *points):
        if len(points) == 0:
            return self
        unzipper = ((p.x, p.y, p.z) for p in points)
        (xs, ys, zs) = zip(*unzipper)
        return self.append_raw(xs, ys, zs)

    def clear(self):
        return self.set(dtype=self._xs.dtype)

    def pen_up(self):
        return self.append_raw(np.nan, np.nan, np.nan)

    def empty(self):
        return len(self._xs) == 0

    def project(self, transform : Callable[[Vector3], Vector2]):
        transformed = [transform(v3) for v3 in self.points()]
        return PolyLine2(transformed)

    def partition(self, predicate : Callable[[Vector3], bool], insert_nan=True):
        pl_true = PolyLine3()
        pl_false = PolyLine3()
        if self.empty():
            return (pl_true, pl_false)

        last_result = predicate(Vector3(self._xs[0], self._ys[0], self._zs[0]))
        for v3 in self.points():
            result = predicate(v3)
            if result:
                pl_true.append(v3)
                if not last_result and insert_nan:
                    pl_false.pen_up()
            else:
                pl_false.append(v3)
                if last_result and insert_nan:
                    pl_true.pen_up()
            last_result = result

        return (pl_false, pl_true)