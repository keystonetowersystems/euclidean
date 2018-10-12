import math

import pytest

from euclidean.R2 import P2, V2


def test_p2_create():
    pass


def test_p2_ccw():
    pass


def test_p2_acute_angle():
    assert math.pi == P2.AcuteAngle(P2(-1, 0), P2(0, 0), P2(1, 0))


def test_p2_vector():
    pass


def test_p2_rotate():
    pass


def test_p2_approx():
    assert P2(1, 1).approx(P2(0.9999999, 0.9999999))
    assert not P2(1, 1).approx(P2(0.999, 0.999))

    with pytest.raises(TypeError):
        P2(0, 0).approx(None)


def test_p2_quadrant():
    assert 1 == P2(1, 1).quadrant()
    assert 1 == P2(0, 0).quadrant()
    assert 1 == P2(0, 1).quadrant()
    assert 1 == P2(1, 0).quadrant()

    assert 2 == P2(-1, 1).quadrant()
    assert 2 == P2(-1, 0).quadrant()

    assert 3 == P2(-1, -1).quadrant()
    assert 3 == P2(0, -1).quadrant()

    assert 4 == P2(1, -1).quadrant()


def test_p2_ordering():
    assert P2(0, 0) < P2(1, 1)
    assert P2(0, 0) < P2(1, 0)
    assert P2(0, 0) < P2(1, -1)

    assert P2(0, 0) > P2(0, -1)

    with pytest.raises(TypeError):
        P2(0, 0) >= V2(0, 0)

    with pytest.raises(TypeError):
        P2(0, 0) > None


def test_p2_add():

    assert P2(1, 1) == P2(0, 0) + V2(1, 1)
    assert P2(1, 1) == V2(1, 1) + P2(0, 0)

    with pytest.raises(TypeError):
        P2(0, 0) + P2(1, 1)


def test_p2_sub():
    assert V2(9, 9) == P2(10, 10) - P2(1, 1)
    assert P2(9, 9) == P2(10, 10) - V2(1, 1)

    with pytest.raises(TypeError):
        P2(10, 10) - 10
