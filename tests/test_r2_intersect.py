import pytest

from euclidean.R2.intersect import intersect

from euclidean.R2.cartesian import P2
from euclidean.R2.circle import Circle
from euclidean.R2.polygon import Polygon
from euclidean.R2.line import Line, LineSegment


def test_line_line():
    l1 = Line(1, 1, 0)
    l2 = Line(1, -1, 0)

    assert {P2(0, 0)} == intersect(l1, l2)

    assert {P2(1, 1)} == intersect(l2, Line(1, 1, 2))


def test_line_line_segment():
    l1 = Line(1, 1, 0)

    assert {P2(0, 0)} == intersect(l1, LineSegment(P2(-10, -10), P2(10, 10)))
    assert {P2(0, 0)} == intersect(LineSegment(P2(-10, -10), P2(10, 10)), l1)
    assert {P2(0, 0)} == intersect(l1, LineSegment(P2(10, 10), P2(-10, -10)))
    assert {P2(0, 0)} == intersect(LineSegment(P2(10, 10), P2(-10, -10)), l1)

    assert set() == intersect(l1, LineSegment(P2(1, 1), P2(10, 10)))


def test_line_segment_line_segment():
    ls1 = LineSegment(P2(0, 0), P2(10, 10))
    ls2 = LineSegment(P2(0, 10), P2(10, 0))

    assert {P2(5, 5)} == intersect(ls1, ls2)
    assert {P2(5, 5)} == intersect(ls2, ls1)

    with pytest.raises(NotImplementedError):
        intersect(ls1, None)

    assert set() == intersect(ls1, LineSegment(P2(0, 5), P2(5, 10)))


def test_line_circle():
    circle = Circle(100, P2(1, 0))
    x = Line(1, 0, 1)

    points = intersect(x, circle)
    assert {P2(1.0, 100.0), P2(1.0, -100.0)} == points

    points = intersect(circle, x)
    assert {P2(1.0, 100.0), P2(1.0, -100.0)} == points

    tangent_circle = Circle(1, P2(2, 0))
    assert {P2(1.0, 0.0)} == intersect(tangent_circle, x)
    assert {P2(1.0, 0.0)} == intersect(x, tangent_circle)


def test_line_segment_circle():
    circle = Circle(100, P2(1, 0))
    x = LineSegment(P2(1, -1000), P2(1, 1000))

    points = intersect(x, circle)
    assert {P2(1.0, 100.0), P2(1.0, -100.0)} == points

    points = intersect(circle, x)
    assert {P2(1.0, 100.0), P2(1.0, -100.0)} == points

    x2 = LineSegment(P2(1, -1000), P2(1, 0))
    assert {P2(1.0, -100.0)} == intersect(circle, x2)

    assert {P2(1.0, -100.0)} == intersect(x2, circle)


def test_circle_circle():
    pass


def test_polygon_line():
    pass


def test_polygon_line_segment():
    pass
