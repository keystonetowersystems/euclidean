import math

import pytest

from euclidean.R2 import P2, V2, Circle


@pytest.fixture
def circle_00():
    return Circle(100)


@pytest.fixture
def circle_11():
    return Circle(100, P2(1, 1))


def test_circle_create(circle_00, circle_11):

    with pytest.raises(ValueError):
        Circle(0)

    with pytest.raises(ValueError):
        Circle(-100)

    assert circle_00.center == P2(0, 0)
    assert circle_00.radius == 100

    assert circle_11.center == P2(1, 1)
    assert circle_11.radius == 100


def test_contains(circle_00, circle_11):

    assert circle_00.contains(P2(0, 0))
    assert circle_11.contains(P2(0, 0))

    assert circle_00.contains(P2(-100, 0))
    assert circle_00.contains(P2(100, 0))
    assert circle_00.contains(P2(0, 100))
    assert circle_00.contains(P2(0, -100))

    assert not circle_00.contains(None)

    assert not circle_00.contains(P2(150, 0))
    assert not circle_00.contains(P2(0, 150))

    assert not circle_11.contains(V2(0, 0))


def test_on_circumference(circle_00, circle_11):
    assert not circle_00.on_circumference(P2(0, 0))
    assert not circle_11.on_circumference(P2(0, 0))

    assert circle_00.on_circumference(P2(100, 0))
    assert circle_00.on_circumference(P2(0, 100))


def test_circumference(circle_00, circle_11):
    assert circle_00.circumference() == circle_11.circumference()
    assert circle_00.circumference() == math.pi * 200


def test_area(circle_00, circle_11):
    a = math.pi * 100 ** 2
    assert a == circle_00.area()
    assert a == circle_11.area()


def test_circle_intersection(circle_00, circle_11):
    far_circle = Circle(100, P2(500, 500))

    with pytest.raises(ValueError):
        circle_00.intersection(circle_00)

    with pytest.raises(TypeError):
        circle_00.intersection(None)

    assert circle_00.intersection(far_circle) == set()
    assert far_circle.intersection(circle_00) == set()

    contained_circle = Circle(50)

    assert circle_00.intersection(contained_circle) == set()
    assert contained_circle.intersection(circle_00) == set()

    tangent_circle = Circle(100, P2(200, 0))
    assert circle_00.intersection(tangent_circle) == {P2(100.0, 0.0)}
    assert tangent_circle.intersection(circle_00) == {P2(100.0, 0.0)}

    intersecting_circle = Circle(100, P2(101, 101))
    assert intersecting_circle.intersection(circle_11) == {
        P2(101.0, 1.0),
        P2(1.0, 101.0),
    }
    assert circle_11.intersection(intersecting_circle) == {
        P2(101.0, 1.0),
        P2(1.0, 101.0),
    }
