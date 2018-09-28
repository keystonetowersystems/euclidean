import numbers

from fuzzyfloat import rel_fp

from euclidean.constants import pi

from .space import P2, V2


class Circle:

    center = property(lambda self: self._center)
    radius = property(lambda self: self._radius)
    diameter = property(lambda self: 2 * self._radius)

    def __init__(self, radius, center=P2(0, 0), c_type=rel_fp):
        """

        (x - center.x) ** 2 + (y - center.y) ** 2 = radius ** 2

        Args:
            radius:
            center (P2):
        """

        assert(radius > 0)
        self._center = center
        self._radius = c_type(radius)

    def circumference(self):
        return pi * self.diameter

    def area(self):
        return pi * self._radius ** 2

    def intersection(self, other):
        if not isinstance(other, Circle):
            raise TypeError()

        if self == other:
            return None  # what should this case return?

        vector = other.center - self.center
        v_mag = vector.magnitude()
        if v_mag > self.radius + other.radius:
            return None  # separate
        if v_mag < abs(self.radius - other.radius):
            return None  # contained

        apothem = (self.radius ** 2 - other.radius ** 2 + v_mag ** 2) / (2 * v_mag)

        intersect_center = self.center + apothem * vector.unit()

        if apothem == self.radius:
            return (intersect_center, )

        h = (self.radius ** 2 - apothem ** 2) ** 0.5
        offset = h * V2(other.center.y - self.center.y, other.center.x - self.center.x) / v_mag
        return (intersect_center + offset, intersect_center - offset)

    def __contains__(self, point):
        if isinstance(point, P2):
            vector = point - self.center
            return vector.magnitude() <= self.radius
        if point is None:
            return False
        return NotImplemented
