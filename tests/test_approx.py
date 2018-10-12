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

    assert P2(-1, -1) not in pset
    assert P2(10, 10) not in pset

    with pytest.raises(TypeError):
        ApproxSet({V2(0, 0), V2(1, 1)})


def test_approx_set_eq():

    pset = ApproxSet([P2(0, 0), P2(1, 1), P2(3, 3)])

    assert {P2(0, 0), P2(1, 1), P2(3, 3)} == pset
    assert {P2(3.0000001, 3.0000001), P2(1, 1), P2(0, 0)} == pset
    assert [P2(3.0000001, 3.0000001), P2(1, 1), P2(0, 0)] == pset
    assert (P2(0.0000001, 0.0000001), P2(1, 1), P2(3, 3)) == pset

    assert pset == pset

    assert [P2(0, 0), P2(1, 1)] != pset

    assert pset != set()

    assert pset != None


def test_approx_set_iter():

    pset = ApproxSet([P2(3, 3), P2(2, 2), P2(1, 1)])

    for e, a in zip([P2(1, 1), P2(2, 2), P2(3, 3)], pset):
        assert e == a


def test_approx_set_create():

    pset = ApproxSet([1, 2, 3, 3.0000001])

    assert 3 == len(pset)
    assert 3.0000001 in pset

    with pytest.raises(TypeError):
        ApproxSet(1, 2, 3)
