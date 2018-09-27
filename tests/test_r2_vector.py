import pytest

from euclidean.constants import eta

from euclidean.R2.space import V2, P2


def test_dot_product():
    v1 = V2(1, 0)
    v2 = V2(0, 1)
    assert v1.dot(v2) == 0
    assert v1.dot(v1) == 1
    assert v2.dot(v2) == 1

    v3 = V2(1, 1)
    assert v3.dot(v3) == 2

    v4 = V2(-2, -2)
    assert v4.dot(v4) == 8


def test_cross_product():
    v1 = V2(1, 0)
    v2 = V2(0, 1)
    assert v1.cross(v2) == 1
    assert v2.cross(v1) == -1
    assert v1.cross(v1) == 0
    assert v2.cross(v2) == 0

    v3 = V2(1, 1)
    assert v3.cross(v1) == -1
    assert v1.cross(v3) == 1
    assert v3.cross(v2) == 1
    assert v2.cross(v3) == -1


def test_add():
    v1 = V2(0, 0)
    v2 = V2(1, 0)
    v3 = V2(0, 1)

    assert v1 + v2 + v3 == V2(1, 1)

    v1 += v2
    assert v1 == V2(1, 0)

    v1 += v3
    assert v1 == V2(1, 1)


def test_sub():
    v1 = V2(100, 100)
    v2 = V2(25, 50)
    v3 = V2(0, 0)

    assert v1 - v2 == V2(75, 50)
    assert v2 - v3 == v2

    v3 -= v1
    assert v3 == V2(-100, -100)


def test_mul():
    v1 = V2(1, 2)
    assert v1 * 2 == V2(2, 4)

    v1 *= -3
    assert v1, V2(-3, -6)


def test_div():
    v1 = V2(1, 2)
    assert v1 / 2 == V2(0.5, 1)

    v1 /= -2
    assert v1 == V2(-0.5, -1)


def test_floordiv():
    v1 = V2(1, 2)
    assert v1 // 2 == V2(0, 1)

    v1 //= 2
    assert v1 == V2(0, 1)


def test_angle():
    pass


def test_parallel():
    pass


def test_orthogonal():
    assert V2(1, 0).is_orthogonal(V2(0, 1))
    assert V2(-1, -1).is_orthogonal(V2(-1, 1))

    assert not V2(1, 0).is_orthogonal(V2(-1, 0))
    assert not V2(1, 1).is_orthogonal(V2(1, 0))


def test_rotate():
    v1 = V2(1, 0)
    v1 = v1.rotate(eta)
    assert v1.x == pytest.approx(0)
    assert v1.y == pytest.approx(1)

    v1 = v1.rotate(eta)
    assert v1.x == pytest.approx(-1)
    assert v1.y == pytest.approx(0)

    v1 = v1.rotate(eta)
    assert v1.x == pytest.approx(0)
    assert v1.y == pytest.approx(-1)

    v1 = v1.rotate(eta)
    assert v1.x == pytest.approx(1)
    assert v1.y == pytest.approx(0)


def test_p2():
    pass
