import pytest

from euclidean.R3 import V3, P3


def test_v3_create():
    vector = V3(1, 2, 3)

    assert 1 == vector.x
    assert 2 == vector.y
    assert 3 == vector.z

    assert V3(1, 2, 3) == vector

    assert P3(1, 2, 3) != vector

    for a, b in zip(vector, [1, 2, 3]):
        assert a == b


def test_v3_magnitude():
    vector = V3(2, 2, 2)

    assert 12 ** 0.5 == vector.magnitude()
    assert 12 ** 0.5 == abs(vector)


def test_v3_dot():
    assert 10 == V3(1, 2, 3).dot(V3(3, 2, 1))
    assert 10 == V3(3, 2, 1).dot(V3(1, 2, 3))

    with pytest.raises(TypeError):
        V3(1, 2, 3).dot(P3(3, 2, 1))


def test_v3_add():

    assert V3(2, 3, 4) == V3(1, 2, 3) + V3(1, 1, 1)

    with pytest.raises(TypeError):
        V3(1, 2, 3) + 5


def test_v3_sub():

    assert V3(0, 0, 0) == V3(3, 2, 1) - V3(3, 2, 1)

    with pytest.raises(TypeError):
        V3(1, 2, 3) - 5


def test_v3_div():

    assert V3(1.5, 2.5, 3.5) == V3(3, 5, 7) / 2

    with pytest.raises(TypeError):
        V3(3, 5, 7) / V3(1, 1, 1)

    assert V3(1, 2, 3) == V3(3, 5, 7) // 2

    with pytest.raises(TypeError):
        V3(3, 5, 7) // V3(1, 1, 1)


def test_v3_neg():

    assert V3(-1, -2, -3) == -V3(1, 2, 3)
