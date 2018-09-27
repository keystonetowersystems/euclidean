import pytest

from euclidean.R2.line import Line, P2, V2

from fuzzyfloat import abs_fp as fp


def test_create_from_points():
    l = Line.ByPoints(P2(-1, -1), P2(1, 1))

    assert l.y(1) == 1
    assert l.y(-1) == -1
    assert l.x(1) == 1
    assert l.x(-1) == -1

    assert l.y(25) == 25
    assert l.y(-25) == -25
    assert l.x(25) == 25
    assert l.x(-25) == -25

    l = Line.ByPoints(P2(-1, 1), P2(1, -1))

    assert l.y(1) == -1
    assert l.y(-1) == 1
    assert l.x(1) == -1
    assert l.x(-1) == 1

    assert l.y(25) == -25
    assert l.y(-25) == 25
    assert l.x(25) == -25
    assert l.x(-25) == 25


def test_degenerate_cases():
    vert = Line.ByPoints(P2(1, 1), P2(1, -1))

    assert vert.y(1) == None
    assert vert.y(-100) == None
    assert vert.x(-1) == 1
    assert vert.x(1) == 1
    assert vert.x(-100) == 1
    assert vert.x(100) == 1

    horz = Line.ByPoints(P2(-1, 0), P2(1, 0))

    assert horz.y(-1) == 0
    assert horz.y(1) == 0
    assert horz.y(-100) == 0
    assert horz.y(100) == 0

    assert horz.x(-1) == None
    assert horz.x(1) == None
    assert horz.x(-100) == None
    assert horz.x(100) == None


def test_intersection():
    horz = Line.ByPoints(P2(fp(-1), fp(10)), P2(fp(1), fp(10)))
    vert = Line.ByPoints(P2(fp(10), fp(-1)), P2(fp(10), fp(1)))

    assert horz.intersection(vert), P2(10, 10)

    assert horz.intersection(horz) == None
    assert horz.intersection(Line.ByPoints(P2(-1, 0), P2(1, 0))) == None

    l45 = Line.ByPoints(P2(0, 0), P2(1, 1))
    assert horz.intersection(l45) == P2(10, 10)

    l135 = Line.ByPoints(P2(0, 0), P2(-1, 1))
    assert horz.intersection(l135) == P2(-10, 10)


def test_closest_point():
    horz = Line.ByPoints(P2(fp(-1), fp(10)), P2(fp(1), fp(10)))

    assert horz.closest(P2(0, 0)) == P2(0, 10)
    assert horz.closest(P2(5, 10)) == P2(5, 10)

    vert = Line.ByPoints(P2(fp(10), fp(1)), P2(fp(10), fp(-2)))

    assert vert.closest(P2(0, 5)) == P2(10, 5)
    assert vert.closest(P2(10, 5)) == P2(10, 5)


def test_translate():
    line = Line(2, 1, 2)
    assert line.y(0) == 2
    assert line.x(0) == 1

    translated = line.translate(V2(1, 1))
    assert translated.y(0) == 3
    assert translated.x(0) == 2

    horz = Line.ByPoints(P2(-1, 10), P2(1, 10))
    assert horz.y(0) == 10

    translated = horz.translate(V2(1, 1))
    assert translated.y(0) == 11

    vert = Line.ByPoints(P2(10, -1), P2(10, 1))
    assert vert.x(0) == 10

    translated = vert.translate(V2(1, 1))
    assert translated.x(0) == 11
