import numbers
import math

from euclidean.vector import v_magnitude, v_angle

class Cartesian2:
    __slots__ = ( '_coords', )

    coords = property(lambda self: self._coords)

    x = property(lambda self: self._coords[0])
    y = property(lambda self: self._coords[1])

    def __init__(self, x, y):
        self._coords = (x, y)

    def __iter__(self):
        return iter(self._coords)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._coords == other._coords
        return NotImplemented

    def __complex__(self):
        return complex(self.x, self.y)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.x, self.y)

    def __hash__(self):
        return hash((self.__class__.__name__, self._coords))

class V2(Cartesian2):
    __slots__ = ()

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x


    def is_parallel(self, other):
        return self.cross(other) == 0

    def is_orthogonal(self, other):
        return self.dot(other) == 0

    def magnitude(self):
        return self.dot(self) ** 0.5

    __abs__ = magnitude

    def angle(self, other):
        return v_angle(self, other)

    def __add__(self, other):
        if isinstance(other, V2):
            return V2(self.x + other.x, self.y + other.y)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, V2):
            return V2(self.x - other.x, self.y - other.y)
        return NotImplemented

    __isub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return V2(self.x * other, self.y * other)
        return NotImplemented

    __imul__ = __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return V2(self.x / other, self.y / other)
        return NotImplemented

    __itruediv__ = __truediv__

    def rotate(self, radians):
        cos = math.cos(radians)
        sin = math.sin(radians)
        return V2(self.x * cos - self.y * sin, self.x * sin + self.y * cos)

class P2(Cartesian2):
    __slots__ = ()

    @staticmethod
    def CCW(p1, p2, p3):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)

    def quadrant(self):
        if self.x >= 0 and self.y >= 0:
            return 1
        if self.x <= 0 and self.y >= 0:
            return 2
        if self.x <= 0 and self.y <= 0:
            return 3
        return 4

    def __add__(self, other):
        if isinstance(other, V2):
            return P2(self.x + other.x, self.y * other.y)
        return NotImplemented

    __iadd__ = __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, V2):
            return P2(self.x - other.x, self.y - other.y)
        if isinstance(other, P2):
            return V2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def vector(self):
        return V2(self.x, self.y)

    def rotate(self, radians, center_point=None):
        center_point = center_point if center_point else P2(0, 0)
        vector = self - center_point
        return center_point + vector.rotate(radians)

