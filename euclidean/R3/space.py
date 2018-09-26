import math, numbers

from euclidean.R2.space import V2, P2

class Cartesian3:
    __slots__ = ( '_coords', )

    def __init__(self, x, y, z):
        self._coords = (x, y, z)

    x = property(lambda self: self._coords[0])
    y = property(lambda self: self._coords[1])
    z = property(lambda self: self._coords[2])

    def __iter__(self):
        return iter(self._coords)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.z)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._coords == other._coords
        return NotImplemented


class V3(Cartesian3):
    __slots__ = ()

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.z
        )

    def magnitude(self):
        return self.dot(self) ** 0.5

    __abs__ = magnitude

    def unit(self):
        return self / self.magnitude()

    def angle(self, other):
        return math.acos(self.dot(other) / self.magnitude() / other.magnitude())

    def xy(self):
        return V2(self.x, self.y)

    def xz(self):
        return V2(self.x, self.z)

    def yz(self):
        return V2(self.y, self.z)

    def __add__(self, other):
        if isinstance(other, V3):
            return V3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, V3):
            return V3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    __isub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return V3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return V3(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, numbers.Real):
            return V3(self.x // other, self.y // other, self.z // other)
        return NotImplemented


class P3(Cartesian3):
    __slots__ = ()

    def __add__(self, other):
        if isinstance(other, V3):
            return P3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, V3):
            return P3(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, P3):
            return V3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    __isub__ = __sub__

    def vector(self):
        return V3(self.x, self.y, self.z)
