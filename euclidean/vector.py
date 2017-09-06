import numpy as np

class Vector:
    __slots__ = ['_coords']

    def __init__(self, *coords, dtype=np.float64):
        self._coords = np.array(coords, dtype=dtype)

    def _new(self, coords):
        constructor = type(self)
        return constructor(*coords, dtype=self._coords.dtype)

    def dot(self, other):
        assert(len(self._coords) == len(other.__coords))
        return self._coords.dot(other._coords)

    def magnitude(self):
        return np.sqrt(self.dot(self))

    def unit(self):
        return self._new(self._coords / self.magnitude())

    def __eq__(self, other):
        return (self._coords == other._coords).all()

    def __neg__(self):
        return self._new(-self._coords)

    def __add__(self, other):
        assert(len(self._coords) == len(other._coords))
        return self._new(self._coords + other._coords)

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        assert(len(self._coords) == len(other._coords))
        return self._new(self._coords - other._coords)

    def __isub__(self, other):
        return self - other

    def __mul__(self, scalar):
        return self._new(self._coords * scalar)

    def __imul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        return self._new(self._coords / scalar)

    def __itruediv__(self, scalar):
        return self / scalar

    def coords(self):
        return self._coords.copy()



class Vector2(Vector):

    def __init__(self, x, y, dtype=np.float64):
        super().__init__(x, y, dtype=dtype)

    @property
    def x(self):
        return self._coords[0]

    @property
    def y(self):
        return self._coords[1]

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def slope(self):
        return self.y / self.x

    def perpendicular(self):
        return self._new([-self.y, self.x])

    def rotate(self, angle):
        cosa = np.cos(angle)
        sina = np.sin(angle)
        return self._new([
            self.x * cosa - self.y * sina,
            self.x * sina + self.y * cosa
        ])

    def rotate_around(self, point, angle):
        new_origin = self - point
        return new_origin.rotate(angle) + point

    def __repr__(self):
        return 'Vector2(%f, %f, dtype=%s)' % (self.x, self.y, self._coords.dtype)

class Vector3(Vector):

    def __init__(self, x, y, z, dtype=np.float64):
        super().__init__(x, y, z, dtype=dtype)

    @property
    def x(self):
        return self._coords[0]

    @property
    def y(self):
        return self._coords[1]

    @property
    def z(self):
        return self._coords[2]

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.z
        )

    def __repr__(self):
        return 'Vector3(%f, %f, %f, dtype=%s)' % (self.x, self.y, self.z, self._coords.dtype)