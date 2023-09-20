import pytest

import math
from euclidean.R2 import Line, P2, V2, Circle, LineSegment, intersect


def test_create():

    with pytest.raises(ValueError):
        Line(0, 0, 0)


def test_line_equality():

    line = Line(1, -1, 0)

    assert line == Line(-1, 1, 0)
    assert line != Line(1, 1, 0)
    assert not line == None


def test_create_from_points():
    l = Line.ByPoints(P2(-1, -1), P2(1, 1))

    assert l.y(1) == pytest.approx(1)
    assert l.y(-1) == pytest.approx(-1)
    assert l.x(1) == pytest.approx(1)
    assert l.x(-1) == pytest.approx(-1)

    assert l.y(25) == pytest.approx(25)
    assert l.y(-25) == pytest.approx(-25)
    assert l.x(25) == pytest.approx(25)
    assert l.x(-25) == pytest.approx(-25)

    l = Line.ByPoints(P2(-1, 1), P2(1, -1))

    assert l.y(1) == pytest.approx(-1)
    assert l.y(-1) == pytest.approx(1)
    assert l.x(1) == pytest.approx(-1)
    assert l.x(-1) == pytest.approx(1)

    assert l.y(25) == pytest.approx(-25)
    assert l.y(-25) == pytest.approx(25)
    assert l.x(25) == pytest.approx(-25)
    assert l.x(-25) == pytest.approx(25)


def test_degenerate_cases():
    vert = Line.ByPoints(P2(1, 1), P2(1, -1))

    assert vert.y(1) is None
    assert vert.y(-100) is None
    assert vert.x(-1) == pytest.approx(1)
    assert vert.x(1) == pytest.approx(1)
    assert vert.x(-100) == pytest.approx(1)
    assert vert.x(100) == pytest.approx(1)

    horz = Line.ByPoints(P2(-1, 0), P2(1, 0))

    assert horz.y(-1) == pytest.approx(0)
    assert horz.y(1) == pytest.approx(0)
    assert horz.y(-100) == pytest.approx(0)
    assert horz.y(100) == pytest.approx(0)

    assert horz.x(-1) is None
    assert horz.x(1) is None
    assert horz.x(-100) is None
    assert horz.x(100) is None


def test_intersection():
    horz = Line.ByPoints(P2(-1, 10), P2(1, 10))
    vert = Line.ByPoints(P2(10, -1), P2(10, 1))

    assert horz.intersection(vert), P2(10, 10)

    assert horz.intersection(horz) is None
    assert horz.intersection(Line.ByPoints(P2(-1, 0), P2(1, 0))) is None

    l45 = Line.ByPoints(P2(0, 0), P2(1, 1))
    assert horz.intersection(l45).approx(P2(10, 10))

    l135 = Line.ByPoints(P2(0, 0), P2(-1, 1))
    assert horz.intersection(l135).approx(P2(-10, 10))


def test_closest_point():
    horz = Line.ByPoints(P2(-1, 10), P2(1, 10))

    assert horz.closest(P2(0, 0)).approx(P2(0, 10))
    assert horz.closest(P2(5, 10)).approx(P2(5, 10))

    vert = Line.ByPoints(P2(10, 1), P2(10, -2))

    assert vert.closest(P2(0, 5)).approx(P2(10, 5))
    assert vert.closest(P2(10, 5)).approx(P2(10, 5))


def test_translate():
    line = Line(2, 1, 2)
    assert line.y(0) == pytest.approx(2)
    assert line.x(0) == pytest.approx(1)

    translated = line.translate(V2(1, 1))
    assert translated.y(0) == pytest.approx(3)
    assert translated.x(0) == pytest.approx(2)

    horz = Line.ByPoints(P2(-1, 10), P2(1, 10))
    assert horz.y(0) == pytest.approx(10)

    translated = horz.translate(V2(1, 1))
    assert translated.y(0) == pytest.approx(11)

    vert = Line.ByPoints(P2(10, -1), P2(10, 1))
    assert vert.x(0) == pytest.approx(10)

    translated = vert.translate(V2(1, 1))
    assert translated.x(0) == pytest.approx(11)


def test_parallel_y():
    line = Line.ByPoints(P2(0, 0), P2(1, 0))

    up_one = line.parallel(P2(1, 1))

    assert up_one == line.parallel(P2(0, 1))

    assert up_one.y(-1) == 1
    assert up_one.y(1) == 1


def test_parallel_x():
    pass


def test_parallel_xy():
    pass


def test_line_contains_point():

    line = Line(1, 1, 0)

    assert line.contains(P2(0, 0))
    assert line.contains(P2(-1, 1))
    assert line.contains(P2(1, -1))

    assert not line.contains(P2(0, 1))

    assert not line.contains(V2(0, 0))


def test_line_intersection():

    l1 = Line(1, 1, 0)
    l2 = Line(1, -1, 0)

    assert l1.intersection(l2) == P2(0, 0)
    assert l2.intersection(l1) == P2(0, 0)

    l3 = Line(1, 1, 1)

    assert l1.intersection(l3) is None

    with pytest.raises(TypeError):
        l1.intersection(None)


def test_line_above():

    horz = Line(0, 1, 10)

    assert horz.on_side(P2(0, 20)) == 1
    assert horz.on_side(P2(20, 20)) == 1

    assert horz.on_side(P2(0, 10)) == 0

    assert horz.on_side(P2(0, 0)) == -1

    vert = Line(1, 0, 10)

    assert vert.on_side(P2(0, 0)) == -1
    assert vert.on_side(P2(20, 0)) == 1
    assert vert.on_side(P2(10, 0)) == 0

    sloped = Line(1, 1, 0)

    assert sloped.on_side(P2(10, 10)) == 1
    assert sloped.on_side(P2(-1, -1)) == -1
    assert sloped.on_side(P2(-10, 20)) == 1
    assert sloped.on_side(P2(-10, 10)) == 0


def test_line_rotation():
    line1 = Line(1, 0, 3)
    line2 = line1.rotate(math.pi/3, P2(1, 2))
    circle = Circle(5)
    p11, p12 = intersect(line1, circle)
    p21, p22 = intersect(line2, circle)
    ls1 = LineSegment(p11, p12)
    ls2 = LineSegment(p21, p22)
    assert ls1.vector().angle(ls2.vector()) == pytest.approx(math.pi/3)

