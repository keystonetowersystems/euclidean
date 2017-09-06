import numpy as np
import matplotlib.pyplot as plt

from .vector import Vector3, Vector2
from .shapes2 import PolyLine2

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

    __slots__ = ['_points']

    def __init__(self, *points):
        self._points = []
        self._points.extend(points)

    def project_xz(self, predicate=lambda p: True):
        return PolyLine2(*[
            Vector2(p.x, p.z)
            for p in self._points
            if predicate(p)
        ])

    def concat(self, polyline):
        assert(isinstance(polyline), PolyLine3)
        self.append(polyline._points)
        return self

    def append(self, *points):
        self._points.extend(points)
        return self

    def draw(self, **kwargs):
        #todo
        xs = [p.x for p in self._points]
        ys = [p.y for p in self._points]
        zs = [p.z for p in self._points]
        plt.plot(xs, ys, zs, **kwargs)