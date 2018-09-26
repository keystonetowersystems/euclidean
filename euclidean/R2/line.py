
from .space import P2, V2

class Line:

    @staticmethod
    def ByPoints(p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        c = dx * p1.y - dy * p1.x
        return Line(-dy, dx, c)

    def __init__(self, cx, cy, c):
        """
        cx * x + cy * y = c
        Args:
            cx:
            cy:
            c:
        """
        assert(cx != 0 or cy != 0)
        self._cx = cx
        self._cy = cy
        self._c = c

    def x(self, y):
        """Find the corresponding x coordinate on the line for coordinate y

        Args:
            y:

        Returns:

        """
        if self._cx == 0:
            return None
        return (self._c - self._cy * y) / self._cx

    def y(self, x):
        """Find the corresponding y coordinate on the line for coordinate x

        Args:
            x:

        Returns:

        """
        if self._cy == 0:
            return None
        return (self._c - self._cx * x) / self._cy

    def perpendicular(self, test_point):
        """Find the line perpendicular to this line, passing through test_point.

        If test_point is on this line, the case is degenerate and returns None

        Args:
            test_point (P2):

        Returns:
            (Line):
        """
        if test_point in self:
            return None
        return Line(-self._cy, self._cx, self._cx * test_point.y - self._cy * test_point.x)

    def parallel(self, test_point):
        """Find the line parallel to this line, passing through test_point.

        Args:
            test_point (P2):

        Returns:
            (Line):
        """
        return Line(self._cx, self._cy, self._cx * test_point.x + self._cy * test_point.y)

    def closest(self, test_point):
        """Find the point on the line closest to the test_point.

        This should be a point that forms a line segment with test point perpendicular to this line.

        Args:
            point (P2):

        Returns:
            (P2): a point on the line
        """
        perpendicular = self.perpendicular(test_point)
        return self.intersection(perpendicular) if perpendicular else test_point

    def __contains__(self, point):
        if isinstance(point, P2):
            return self._cx * point.x + self._cy * point.y ==  self._c
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Line):
            return self._cx == other._cx and self._cy == other._cy and self._c == other._c
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def intersection(self, other):
        if isinstance(other, Line):
            det = self._cx * other._cy - self._cy * other._cx
            if det == 0:
                return None
            return P2(
                (other._cy * self._c - self._cy * other._c) / det,
                (self._cx * other._c - other._cx * self._c) / det
            )
        raise TypeError()

class LineSegment:

    def __init__(self, p1, p2):
        assert(p1 != p2)
        self._p1 = p1
        self._p2 = p2

    def vector(self):
        return self._p2 - self._p1

    def length(self):
        return self.vector().magnitude()

    def ordered(self):
        return (self._p1, self._p2) if self._p1._coords < self._p2._coords else (self._p2, self._p1)

    def __contains__(self, point):
        if isinstance(point, P2):
            line_vector = self.vector()
            test_vector = point - self._p1
            if not line_vector.is_parallel(test_vector):
                return False
            return 0 <= line_vector.dot(test_vector) <= line_vector.dot(line_vector)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, LineSegment):
            return self.ordered() == other.ordered()
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def line(self):
        return Line.ByPoints(self._p1, self._p2)

    def intersection(self, other):
        if not isinstance(other, LineSegment):
            raise TypeError()
        if not self.does_intersect(other):
            return None
        return self.line().intersection(other.line())

    def does_intersect(self, other):
        if P2.CCW(self._p1, self._p2, other._p1) * P2.CCW(self._p1, self._p2, other._p2) > 0:
            return False
        if P2.CCW(other._p1, other._p2, self._p1) * P2.CCW(other._p1, other._p2, self._p2) > 0:
            return False
        return True

    def __hash__(self):
        return hash(self.ordered())

    def __str__(self):
        return '(%s, %s)' % (self._p1, self._p2)

    def __repr__(self):
        return 'LineSegment(%r, %r)' % (self._p1, self._p2)