import pytest

from euclidean.R3 import P3, V3, Plane


def test_plane_create():
    plane = Plane.PointNormal(P3(0, 0, 0), V3(1, 1, 1))

    assert Plane(1, 1, 1, 0) == plane
    assert None != plane


def test_plane_contains():
    plane = Plane(1, 1, 1, 0)

    assert plane.contains(P3(0, 0, 0))

    assert plane.contains(P3(-1, 1, 0))
    assert plane.contains(P3(-1, 0, 1))

    with pytest.raises(TypeError):
        plane.contains(V3(0, 0, 0))


def test_plane_normal():
    plane = Plane(1, 1, 1, 1)

    assert V3(1, 1, 1).unit() == plane.normal()
