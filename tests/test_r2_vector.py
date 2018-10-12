import pytest

from euclidean.constants import eta

from euclidean.R2 import V2


def test_v2_polar():
    assert V2(1, 0).approx(V2.Polar(1, 0))
    assert V2(0, 1).approx(V2.Polar(1, eta))
    assert V2(-1, 0).approx(V2.Polar(1, 2 * eta))
    assert V2(0, -1).approx(V2.Polar(1, 3 * eta))
    assert V2(1, 0).approx(V2.Polar(1, 4 * eta))


def test_v2_eq():
    assert V2(1, 1) == V2(1, 1)
    assert not V2(1, 1) == V2(0, 0)
    assert not None == V2(1, 1)

    assert V2(0.9999999, 0.9999999).approx(V2(1, 1))
    assert not V2(0.9, 0.9).approx(V2(1, 1))

    with pytest.raises(TypeError):
        V2(1, 1).approx(None)


def test_v2_iter():
    it = iter(V2(1, 2))
    assert 1 == next(it)
    assert 2 == next(it)

    with pytest.raises(StopIteration):
        next(it)


def test_v2_repr():
    assert repr(V2(1, 0)) == "V2(1, 0)"


def test_v2_dot_product():
    v1 = V2(1, 0)
    v2 = V2(0, 1)
    assert v1.dot(v2) == pytest.approx(0)
    assert v1.dot(v1) == pytest.approx(1)
    assert v2.dot(v2) == pytest.approx(1)

    v3 = V2(1, 1)
    assert v3.dot(v3) == pytest.approx(2)

    v4 = V2(-2, -2)
    assert v4.dot(v4) == pytest.approx(8)


def test_cross_product():
    v1 = V2(1, 0)
    v2 = V2(0, 1)
    assert v1.cross(v2) == pytest.approx(1)
    assert v2.cross(v1) == pytest.approx(-1)
    assert v1.cross(v1) == pytest.approx(0)
    assert v2.cross(v2) == pytest.approx(0)

    v3 = V2(1, 1)
    assert v3.cross(v1) == pytest.approx(-1)
    assert v1.cross(v3) == pytest.approx(1)
    assert v3.cross(v2) == pytest.approx(1)
    assert v2.cross(v3) == pytest.approx(-1)


def test_add():
    v1 = V2(0, 0)
    v2 = V2(1, 0)
    v3 = V2(0, 1)

    assert V2(1, 1).approx(v1 + v2 + v3)

    v1 += v2
    assert V2(1, 0).approx(v1)

    v1 += v3
    assert V2(1, 1).approx(v1)

    with pytest.raises(TypeError):
        v1 + None


def test_v2_sub():
    v1 = V2(100, 100)
    v2 = V2(25, 50)
    v3 = V2(0, 0)

    assert V2(75, 50).approx(v1 - v2)
    assert v2.approx(v2 - v3)

    v3 -= v1
    assert V2(-100, -100).approx(v3)

    with pytest.raises(TypeError):
        v3 - None


def test_v2_mul():
    v1 = V2(1, 2)
    assert V2(2, 4).approx(v1 * 2)
    assert V2(2, 4).approx(2 * v1)

    v1 *= -3
    assert V2(-3, -6).approx(v1)

    with pytest.raises(TypeError):
        v1 * None


def test_div():
    v1 = V2(1, 2)
    assert V2(0.5, 1).approx(v1 / 2)

    v1 /= -2
    assert V2(-0.5, -1).approx(v1)

    with pytest.raises(TypeError):
        v1 / None


def test_floordiv():
    v1 = V2(1, 2)
    assert V2(0, 1).approx(v1 // 2)

    v1 //= 2
    assert V2(0, 1).approx(v1)

    with pytest.raises(TypeError):
        v1 // None


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
    assert V2(0, 1).approx(v1)

    v1 = v1.rotate(eta)
    assert V2(-1, 0).approx(v1)

    v1 = v1.rotate(eta)
    assert V2(0, -1).approx(v1)

    v1 = v1.rotate(eta)
    assert V2(1, 0).approx(v1)


def test_p2():
    pass
