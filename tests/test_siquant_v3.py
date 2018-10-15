import pytest

from siquant import SIUnit, si, make

from euclidean.constants import eta
from euclidean.siquant.factory import make_factory, V2Quantity, V3Quantity

from euclidean.R2 import V2
from euclidean.R3 import V3

SIUnit.factory = make_factory(V2Quantity, V3Quantity)


def test_create():

    xyz = make(V3(1, 2, 3), si.meters)

    assert V3(1, 2, 3) * si.meters == xyz
    assert V3(1, 2, 3) == xyz.get_as(si.meters)
    assert V3(1000, 2000, 3000) == xyz.get_as(si.millimeters)

    assert V2(1, 2) * si.meters == xyz.xy()
    assert V2(2, 3) * si.meters == xyz.yz()
    assert V2(1, 3) * si.meters == xyz.xz()


def test_cmp():
    xyz = V3(1, 2, 3) * si.meters

    assert not V3(1, 2, 3) == xyz
    assert not None == xyz


def test_angle():
    x = V3(1, 0, 0) * si.meters
    y = V3(0, 1, 0) * si.millimeters

    assert pytest.approx(eta) == x.angle(y).get_as(si.radians)

    z = V3(0, 0, 1) * si.meters

    assert pytest.approx(eta) == x.angle(z).get_as(si.radians)


def test_v3_cross():
    x = V3(1, 0, 0) * si.meters
    y = V3(0, 1, 0) * si.meters

    assert make(V3(0, 0, 1), si.meters ** 2).approx(x.cross(y))
    assert make(V3(0, 0, -1), si.meters ** 2).approx(y.cross(x))


def test_v3_manhattan_distance():
    xyz = V3(1, 2, 3) * si.meters

    assert 6 * si.meters == xyz.manhattan_distance()


def test_v3_magnitude():
    xyz = V3(1, 1, 1) * si.meters

    assert pytest.approx(3 ** 0.5) == xyz.magnitude().get_as(si.meters)


def test_v3_unit():
    xyz = V3(1, 2, 3) * si.meters

    assert pytest.approx(1) == xyz.unit().magnitude().quantity


def test_v3_add():
    xyz = V3(1, 2, 3) * si.meters

    assert make(V3(2, 4, 6), si.meters).approx(xyz + xyz)

    with pytest.raises(TypeError):
        xyz + V3(1, 2, 3)


def test_v3_sub():
    xyz = V3(1, 2, 3) * si.meters

    assert make(V3(0, 0, 0), si.meters).approx(xyz - xyz)

    with pytest.raises(TypeError):
        xyz - V3(1, 2, 3)


def test_v3_mul():
    xyz = V3(1, 2, 3) * si.meters

    assert make(V3(2, 4, 6), si.meters).approx(xyz * 2)
    assert make(V3(2, 4, 6), si.meters).approx(2 * xyz)

    with pytest.raises(TypeError):
        xyz * xyz


def test_v3_div():
    xyz = V3(2, 4, 6) * si.meters

    assert make(V3(1, 2, 3), si.meters).approx(xyz / 2)

    with pytest.raises(TypeError):
        2 / xyz

    with pytest.raises(TypeError):
        xyz / None
