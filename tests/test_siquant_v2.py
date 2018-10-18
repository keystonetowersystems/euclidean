import pytest

from euclidean.constants import eta

from siquant import SIUnit, make, si

from euclidean.siquant.factory import V2Quantity, make_factory

from euclidean.R2 import V2

SIUnit.factory = make_factory(V2Quantity)


def test_qv2_create():
    vector = V2(1, 0)

    vector_q = make(vector, si.meters)

    assert vector == vector_q.get_as(si.meters)
    assert V2(1000, 0) == vector_q.get_as(si.millimeters)

    vector_q = vector * si.meters
    assert vector == vector_q.get_as(si.meters)

    vector_q = si.meters * vector
    assert vector == vector_q.get_as(si.meters)


def test_qv2_rotate():
    vector = V2(1, 0)
    qv2 = make(vector, si.meters)

    qv2 = qv2.rotate(eta * si.radians)
    assert make(V2(0, 1), si.meters).approx(qv2)

    qv2 = qv2.rotate(eta * si.radians)
    assert make(V2(-1, 0), si.meters).approx(qv2)

    qv2 = qv2.rotate(eta * si.radians)
    assert make(V2(0, -1), si.meters).approx(qv2)


def test_qv2_dot_product():
    qv2 = make(V2(3, 4), si.meters)

    dot_product = qv2.dot(qv2)
    assert not isinstance(dot_product, V2Quantity)
    assert 25 == dot_product.get_as(si.meters ** 2)


def test_qv2_cross_product():
    qv2 = make(V2(1, 1), si.meters)

    cross_product = qv2.cross(qv2)
    assert not isinstance(cross_product, V2Quantity)
    assert 0 == cross_product.get_as(si.meters ** 2)


def test_qv2_magnitude():
    qv2 = make(V2(3, 4), si.meters)

    assert 5 == qv2.magnitude().get_as(si.meters)


def test_qv2_is_parallel():
    qv2 = make(V2(1, 1), si.meters)

    assert qv2.is_parallel(make(V2(2, 2), si.meters))
    assert qv2.is_parallel(make(V2(-1, -1), si.meters))

    assert not qv2.is_parallel(make(V2(1, 0), si.meters))
    assert not qv2.is_parallel(make(V2(0, 1), si.meters))

    assert qv2.is_parallel(V2(2, 2))
    assert qv2.is_parallel(V2(-1, -1))

    assert not qv2.is_parallel(V2(1, 0))
    assert not qv2.is_parallel(V2(0, 1))

    with pytest.raises(TypeError):
        V2(1, 1).is_parallel(qv2)


def test_qv2_is_orthogonal():
    qv2 = make(V2(1, 1), si.meters)

    assert qv2.is_orthogonal(make(V2(-1, 1), si.meters))
    assert qv2.is_orthogonal(V2(-1, 1))

    assert not qv2.is_orthogonal(make(V2(1, 0), si.meters))
    assert not qv2.is_orthogonal(V2(1, 0))

    with pytest.raises(TypeError):
        V2(1, 0).is_orthogonal(qv2)


def test_qv2_angle():
    qv_x = make(V2(1, 0), si.meters)
    qv_y = make(V2(0, 1), si.meters)
    qv_xy = make(V2(1, 1), si.meters)

    assert pytest.approx(eta) == qv_x.angle(qv_y).get_as(si.radians)
    assert pytest.approx(eta / 2) == qv_x.angle(qv_xy).get_as(si.radians)
    assert pytest.approx(eta / 2) == qv_y.angle(qv_xy).get_as(si.radians)

    assert pytest.approx(eta) == qv_x.angle(V2(0, 1)).get_as(si.radians)

    with pytest.raises(TypeError):
        V2(0, 1).angle(qv_x)


def test_qv2_manhattan_dinstance():
    qv2 = make(V2(10, 10), si.meters)

    assert 20 == qv2.manhattan_distance().get_as(si.meters)
    assert 20000 == qv2.manhattan_distance().get_as(si.millimeters)


def test_qv2_unit():

    qv2 = make(V2(100, 0), si.meters)

    assert make(V2(1, 0), si.unity) == qv2.unit()

    qv2 = qv2.cvt_to(si.millimeters)

    assert make(V2(1, 0), si.unity) == qv2.unit()

    assert qv2 == abs(qv2) * qv2.unit()


def test_qv2_mul():
    qv2 = make(V2(3, 4), si.meters)

    mul_value = qv2 * 2
    assert V2(6, 8).approx(mul_value.get_as(si.meters))

    mul_value = 2 * qv2
    assert V2(6, 8).approx(mul_value.get_as(si.meters))

    qv2 *= 2
    assert V2(6, 8).approx(qv2.get_as(si.meters))


def test_qv2_div():
    qv2 = make(V2(11, 21), si.meters)

    div_value = qv2 / 2
    assert V2(5.5, 10.5).approx(div_value.get_as(si.meters))

    qv2 /= 2
    assert V2(5.5, 10.5).approx(qv2.get_as(si.meters))
