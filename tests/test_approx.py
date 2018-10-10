import pytest

from euclidean.approx import ApproxSet, approx

from euclidean.R2 import V2, P2


def test_approx():

    assert approx(P2(0, 0), P2(0.0, 0.0))
    assert approx(P2(0.0000001, 0.0000001), P2(0, 0))
    assert not approx(P2(0, 0), V2(0, 0))


def test_approx_set_contains():

    pset = ApproxSet({P2(0, 0), P2(1, 1), P2(3, 3)})

    assert P2(0, 0) in pset
    assert P2(0.0, 0.0) in pset
    assert P2(0.0000001, 0.0000001) in pset

    assert P2(0.1, 0.1) not in pset

    with pytest.raises(TypeError):
        ApproxSet({V2(0, 0), V2(1, 1)})


def test_approx_set_eq():

    pset = ApproxSet([P2(0, 0), P2(1, 1), P2(3, 3)])

    assert {P2(0, 0), P2(1, 1), P2(3, 3)} == pset
    assert {P2(3.0000001, 3.0000001), P2(1, 1), P2(0, 0)} == pset
    assert [P2(3.0000001, 3.0000001), P2(1, 1), P2(0, 0)] == pset
    assert (P2(0.0000001, 0.0000001), P2(1, 1), P2(3, 3)) == pset

    assert [P2(0, 0), P2(1, 1)] != pset
