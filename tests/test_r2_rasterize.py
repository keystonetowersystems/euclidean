import pytest

from euclidean.R2 import rasterize
from euclidean.R2 import P2, LineSegment, Circle, Polygon
from euclidean.approx import ApproxSet


@pytest.fixture
def square():
    return Polygon([P2(0, 0), P2(1, 0), P2(1, 1), P2(0, 1)])


def test_rasterize_polygon_8(square):
    expected = ApproxSet(
        [
            P2(0, 0),
            P2(0.5, 0),
            P2(1, 0),
            P2(1, 0.5),
            P2(1, 1),
            P2(0.5, 1),
            P2(0, 1),
            P2(0, 0.5),
        ]
    )
    assert expected == rasterize(square, n=8)


def test_rasterize_polygon_12(square):
    expected = ApproxSet(
        [
            P2(0, 0),
            P2(0.3333333, 0),
            P2(0.6666666, 0),
            P2(1, 0),
            P2(1, 0.3333333),
            P2(1, 0.6666666),
            P2(1, 1),
            P2(0.6666666, 1),
            P2(0.3333333, 1),
            P2(0, 1),
            P2(0, 0.6666666),
            P2(0, 0.3333333),
        ]
    )
    assert expected == rasterize(square, n=12)


def test_rasterize_polygon_10(square):
    expected = ApproxSet(
        [
            P2(0, 0),
            P2(0.5, 0),
            P2(1, 0),
            P2(1, 0.3333333),
            P2(1, 0.6666666),
            P2(1, 1),
            P2(0.5, 1),
            P2(0, 1),
            P2(0, 0.6666666),
            P2(0, 0.3333333),
        ]
    )
    assert expected == rasterize(square, n=10)


def test_rasterize_polygon_4(square):
    expected = ApproxSet([P2(0, 0), P2(1, 0), P2(1, 1), P2(0, 1)])
    assert expected == rasterize(square, n=4)


def test_rasterize_polygon_fail(square):
    with pytest.raises(AssertionError):
        rasterize(square, n=3)


def test_rasterize_polygon_15(square):
    expected = ApproxSet(
        [
            P2(0, 0),
            P2(0.3333333, 0),
            P2(0.6666666, 0),
            P2(1, 0),
            P2(1, 0.25),
            P2(1, 0.5),
            P2(1, 0.75),
            P2(1, 1),
            P2(0.75, 1),
            P2(0.5, 1),
            P2(0.25, 1),
            P2(0, 1),
            P2(0, 0.75),
            P2(0, 0.5),
            P2(0, 0.25),
        ]
    )
    assert expected == rasterize(square, n=15)


def test_rasterize_line_segment():
    expected = ApproxSet([P2(0, 0), P2(1, 0), P2(2, 0), P2(3, 0)])
    assert expected == rasterize(LineSegment(P2(0, 0), P2(3, 0)), n=4)


def test_rasterize_circle():
    expected = ApproxSet([P2(1, 0), P2(0, 1), P2(-1, 0), P2(0, -1)])
    assert expected == rasterize(Circle(1), n=4)

    expected = ApproxSet([P2(2, 1), P2(1, 2), P2(0, 1), P2(1, 0)])
    assert expected == rasterize(Circle(1, P2(1, 1)), n=4)
