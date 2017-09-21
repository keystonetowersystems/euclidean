import numpy as np
import matplotlib.pyplot as plt

from collections.abc import Iterable

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

    def __init__(self, *points, dtype=np.float64):
        self._xs = np.array([p.x for p in points], dtype=dtype)
        self._ys = np.array([p.y for p in points], dtype=dtype)
        self._zs = np.array([p.z for p in points], dtype=dtype)

    def _points(self):
        return zip(self._xs, self._ys, self._zs)

    def project_xz(self, predicate=lambda p: True):
        polyline2 = PolyLine2()
        indices = [predicate(Vector3(x, y, z)) for (x, y, z) in self._points()]
        polyline2.append_raw(self._xs[indices], self._zs[indices])
        return polyline2

    def filter(self, predicate=lambda p: True):
        indices = [predicate(Vector3(x, y, z) for (x, y, z) in self._points())]
        self._xs = self._xs[indices]
        self._ys = self._ys[indices]
        self._zs = self._zs[indices]
        return self

    def concat(self, polyline):
        assert(isinstance(polyline, PolyLine3))
        return self.append_raw(polyline._xs, polyline._ys, polyline._zs)

    def append_raw(self, xs, ys, zs):
        self._xs = np.append(self._xs, xs)
        self._ys = np.append(self._ys, ys)
        self._zs = np.append(self._zs, zs)
        return self

    def append(self, *points):
        return self.append_raw(
            (p.x for p in points),
            (p.y for p in points),
            (p.z for p in points)
        )

    def clear(self):
        self._xs = np.array([], dtype=self._xs.dtype)
        self._ys = np.array([], dtype=self._ys.dtype)
        self._zs = np.array([], dtype=self._zs.dtype)

    def empty(self):
        return len(self._xs) == 0

    def draw(self, **kwargs):
        plt.plot(self._xs, self._ys, self._zs, **kwargs)

class PolyLineSet3(Iterable):

    def __init__(self, *polylines3):
        self.polyline_set = set()
        for polyline in polylines3:
            self.add_polyline(polyline)

    def add_polyline(self, polyline):
        assert(isinstance(polyline, PolyLine3))
        self.polyline_set.add(polyline)

    def project_xz(self, predicate=lambda p: True):
        polyline_set = PolyLineSet2()
        for polyline in self.polyline_set:
            polyline_set.add_polyline(polyline.project_xz(predicate))
        return polyline_set

    def __iter__(self):
        return iter(self.polyline_set)


