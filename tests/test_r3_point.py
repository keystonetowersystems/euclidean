import pytest

from euclidean.R3 import P3, V3


def test_p3_create():
    point = P3(1, 2, 3)
    assert 1 == point.x
    assert 2 == point.y
    assert 3 == point.z

    assert V3(1, 2, 3) == point.vector()


def test_p3_approx():
    point = P3(1, 2, 3)

    assert point.approx(P3(1, 2, 3))
    assert point.approx(P3(0.99999999, 1.99999999, 2.99999999))

    assert not point.approx(P3(0.999, 1.999, 2.999))

    with pytest.raises(TypeError):
        point.approx(V3(1, 2, 3))


def test_p3_add():
    point = P3(1, 2, 3)

    assert P3(2, 3, 4) == point + V3(1, 1, 1)
    assert P3(2, 3, 4) == V3(1, 1, 1) + point

    with pytest.raises(TypeError):
        point + point


def test_p3_sub():
    point = P3(1, 2, 3)

    assert P3(0, 1, 2) == point - V3(1, 1, 1)
    assert V3(0, 0, 0) == point - point

    with pytest.raises(TypeError):
        point - 1


def test_p3_ordering():

    assert P3(0, 1, 1) < P3(1, 1, 1)
    assert P3(0, 1, 1) < P3(1, 0, 0)
    assert P3(0, 1, 1) < P3(1, -1, -1)

    assert P3(1, 0, 0) < P3(1, 1, 1)
    assert P3(1, 1, 0) < P3(1, 1, 1)

    with pytest.raises(TypeError):
        P3(0, 1, 2) < V3(1, 2, 3)
