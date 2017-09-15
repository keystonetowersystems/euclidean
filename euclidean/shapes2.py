import numpy as np
import matplotlib.pyplot as plt

from .vector import Vector2

DEFAULT_EPSILON = 0.00001


class Shape2:

    def intersect_line(self, line):
        pass

    def intersect_line_segment(self, line_segment):
        pass

    def contains(self, point):
        pass

class Line2:

    __slots__ = ['_point', '_vector']

    def __init__(self, point, vector):
        assert(isinstance(point, Vector2))
        assert(isinstance(point, Vector2))
        assert(vector.x != 0 or vector.y != 0)
        self._point = point
        self._vector = vector

    def slope(self):
        return self._vector.slope()

    def y_intercept(self):
        return self._point.y - self._point.x * self.slope()

    def is_parallel(self, other, epsilon=DEFAULT_EPSILON):
        return self.slope() - other.slope() < epsilon

    def approx_equal(self, other, epsilon=DEFAULT_EPSILON):
        return self.is_parallel(other, epsilon) and \
            self.y_intercept() - other.y_intercept() < epsilon

    def intersect_line(self, other):
        assert(isinstance(other, Line2))
        a = self.slope()
        c = self.y_intercept()

        b = other.slope()
        d = other.y_intercept()

        if a == b:
            return None

        x = (d - c) / (a - b)
        y = a * x + c

        return self._point._new([x, y])

    def intersect_line_segment(self, line_segment):
        point = self.intersect_line(line_segment.line())
        if line_segment.contains(point):
            return point
        return None

    def perpendicular_line(self, point):
        assert(isinstance(point, Vector2))
        return Line2(point, self._vector.perpendicular())

    def perpendicular_point(self, point):
        return self.intersect_line(self.perpendicular_line(point))

    def translate(self, vector):
        return Line2(self._point + vector, self._vector)

class LineSegment2:

    __slots__ = ['_p1', '_p2']

    def __init__(self, p1, p2):
        assert(isinstance(p1, Vector2))
        assert(isinstance(p2, Vector2))
        self._p1 = p1
        self._p2 = p2

    def vector(self):
        return self._p2 - self._p1

    def line(self):
        return Line2(self._p1, self.vector())

    def length(self):
        return self.vector().magnitude()

    def translate(self, vector):
        return LineSegment2(self._p1 + vector, self._p2 + vector)

    def contains(self, point):
        return point in self

    def __contains__(self, point):
        assert(isinstance(point, Vector2))
        v1 = point - self._p1
        v2 = point - self._p2
        path_dist = v1.magnitude() + v2.magnitude()
        dist_diff = path_dist - self.length()
        return dist_diff < DEFAULT_EPSILON

    def intersect_line_segment(self, line_segment):
        point = self.intersect_line(line_segment.line())
        if point == None or point not in line_segment:
            return None
        return point

    def intersect_line(self, line):
        point = self.line().intersect_line(line)
        if point == None or point not in self:
            return None
        return point

    def intersect_circle(self, circle):
        return [p for p in circle.intersect_line(self.line()) if self.contains(p)]

    def draw(self, **kwargs):
        plt.plot([self._p1.x, self._p2.x], [self._p1.y, self._p2.y], **kwargs)


    def polyline(self, n=2):
        assert(n >= 2)
        polyline = PolyLine2()
        polyline.append_raw(
            np.linspace(self._p1.x, self._p2.x, n),
            np.linspace(self._p1.y, self._p2.y, n)
        )
        return polyline

class Circle:

    __slots__ = ['center', 'radius']

    def __init__(self, center=Vector2(0,0), radius=1):
        assert(isinstance(center, Vector2))
        assert(radius > 0)
        self.center = center
        self.radius = radius

    def intersect_line(self, line):
        result = []
        line_ = line.translate(self.center * -1)
        dx = line_.p2.x - line_.p1.x
        dy = line_.p2.y - line_.p1.y
        dr = line_.length()
        D = np.linalg.det(
            np.matrix([
                [line_.p1.x, line_.p1.y],
                [line_.p2.x, line_.p2.y]
            ])
        )

        dr2 = dr**2
        discriminant = self.radius**2 * dr2 - D**2
        if discriminant < 0:
            return result


        x0 = D * dy / dr2
        y0 = -D * dx / dr2
        if discriminant == 0:
            result.append(Vector2(x0, y0) + self.center)
            return result

        sqrt_discriminant = np.sqrt(discriminant)
        x_off = np.sign(dy) * dx * sqrt_discriminant / dr2
        y_off = np.abs(dy) * sqrt_discriminant / dr2

        result.append(self.center + Vector2(x0 + x_off, y0 + y_off))
        result.append(self.center + Vector2(x0 - x_off, y0 - y_off))
        return result

    def intersect_line_segment(self, line_segment):
        points = self.intersect_line(line_segment.line())
        return [p for p in points if line_segment.contains(p)]

class PolyLine2:

    __slots__ = ['_xs', '_ys']

    def __init__(self, *points, dtype=np.float64):
        self._xs = np.array([p.x for p in points], dtype=dtype)
        self._ys = np.array([p.y for p in points], dtype=dtype)

    def concat(self, polyline):
        assert(isinstance(polyline, PolyLine2))
        self._xs = np.append(self._xs, polyline._xs)
        self._ys = np.append(self._ys, polyline._ys)
        return self

    def append(self, *points):
        assert(all([isinstance(p, Vector2) for p in points]))
        self.append_raw([p.x for p in points], [p.y for p in points])
        return self

    def append_raw(self, xs, ys):
        self._xs = np.append(self._xs, xs)
        self._ys = np.append(self._ys, ys)
        return self

    def draw(self, **kwargs):
        plt.plot(self._xs, self._ys, **kwargs)
        return self

    def area(self):
        # NOTE: THIS WILL ONLY WORK FOR A WELL FORMED SIMPLE POLYGON!
        return 0.5 * np.abs(np.dot(self._xs, np.roll(self._ys, 1)) - np.dot(self._ys, np.roll(self._xs, 1)))

    def reverse(self):
        self._xs = np.fliplr(self._xs)
        self._ys = np.fliplr(self._ys)
        return self

class PolyLineSet2:

    def __init__(self, *polylines2):
        self.polyline_set = set()
        for polyline in polylines2:
            self.add_polyline(polyline)

    def add_polyline(self, polyline2):
        assert(isinstance(polyline2, PolyLine2))
        self.polyline_set.add(polyline2)

    def draw(self, **kwargs):
        for polyline in self.polyline_set:
            polyline.draw(**kwargs)


class Arc2:

    def __init__(self, center=Vector2(0,0), radius=1, theta=np.pi):
        self.center = center
        self.radius = radius
        self.theta = theta

    def polyline(self, n=50):
        polyline = PolyLine2()