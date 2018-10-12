import math

import pytest

from euclidean.R2 import P2, Polygon, V2

from euclidean.R2.polygon.polygon import _standard_form
from euclidean.R2.polygon.hull import _jarvis_convex_hull, convex_hull

from euclidean.approx import ApproxSet


@pytest.fixture
def ccw_polygon():
    return Polygon([P2(0, 0), P2(1, 0), P2(1, 1), P2(0, 1)])


@pytest.fixture
def cw_polygon():
    return Polygon([P2(0, 0), P2(0, 1), P2(1, 1), P2(1, 0)])


@pytest.fixture
def ccw_intersecting():
    return Polygon([P2(0, 0), P2(1, 1), P2(0, 1), P2(1, 0)])


@pytest.fixture
def cw_intersecting():
    return Polygon([P2(0, 0), P2(1, 1), P2(1, 0), P2(0, 1)])


@pytest.fixture
def cw_concave():
    return Polygon([P2(-1, -1), P2(1, -1), P2(0, 0), P2(1, 1), P2(-1, 1)])


@pytest.fixture
def hull_data():
    point_cloud = [
        P2(0.3215348546593775, 0.03629583077160248),
        P2(0.02402358131857918, -0.2356728797179394),
        P2(0.04590851212470659, -0.4156409924995536),
        P2(0.3218384001607433, 0.1379850698988746),
        P2(0.11506479756447, -0.1059521474930943),
        P2(0.2622539999543261, -0.29702873322836),
        P2(-0.161920957418085, -0.4055339716426413),
        P2(0.1905378631228002, 0.3698601009043493),
        P2(0.2387090918968516, -0.01629827079949742),
        P2(0.07495888748668034, -0.1659825110491202),
        P2(0.3319341836794598, -0.1821814101954749),
        P2(0.07703635755650362, -0.2499430638271785),
        P2(0.2069242999022122, -0.2232970760420869),
        P2(0.04604079532068295, -0.1923573186549892),
        P2(0.05054295812784038, 0.4754929463150845),
        P2(-0.3900589168910486, 0.2797829520700341),
        P2(0.3120693385713448, -0.0506329867529059),
        P2(0.01138812723698857, 0.4002504701728471),
        P2(0.009645149586391732, 0.1060251100976254),
        P2(-0.03597933197019559, 0.2953639456959105),
        P2(0.1818290866742182, 0.001454397571696298),
        P2(0.444056063372694, 0.2502497166863175),
        P2(-0.05301752458607545, -0.06553921621808712),
        P2(0.4823896228171788, -0.4776170002088109),
        P2(-0.3089226845734964, -0.06356112199235814),
        P2(-0.271780741188471, 0.1810810595574612),
        P2(0.4293626522918815, 0.2980897964891882),
        P2(-0.004796652127799228, 0.382663812844701),
        P2(0.430695573269106, -0.2995073500084759),
        P2(0.1799668387323309, -0.2973467472915973),
        P2(0.4932166845474547, 0.4928094162538735),
        P2(-0.3521487911717489, 0.4352656197131292),
        P2(-0.4907368011686362, 0.1865826865533206),
        P2(-0.1047924716070224, -0.247073392148198),
        P2(0.4374961861758457, -0.001606279519951237),
        P2(0.003256207800708899, -0.2729194320486108),
        P2(0.04310378203457577, 0.4452604050238248),
        P2(0.4916198379282093, -0.345391701297268),
        P2(0.001675087028811806, 0.1531837672490476),
        P2(-0.4404289572876217, -0.2894855991839297),
    ]

    hull = [
        P2(-0.161920957418085, -0.4055339716426413),
        P2(0.4823896228171788, -0.4776170002088109),
        P2(0.4916198379282093, -0.345391701297268),
        P2(0.4932166845474547, 0.4928094162538735),
        P2(0.05054295812784038, 0.4754929463150845),
        P2(-0.3521487911717489, 0.4352656197131292),
        P2(-0.4907368011686362, 0.1865826865533206),
        P2(-0.4404289572876217, -0.2894855991839297),
    ]

    return (point_cloud, hull)


def test_polygon_create():

    with pytest.raises(ValueError):
        Polygon([P2(0, 0), P2(20, 20)])


def test_polygon_eq(cw_polygon, ccw_polygon):
    assert cw_polygon == cw_polygon
    assert cw_polygon != ccw_polygon  # we may want to fix this
    assert not cw_polygon == None
    assert not cw_polygon == Polygon([P2(0, 0), P2(1, 1), P2(0, 1)])


def test_polygon_translate(cw_polygon, ccw_polygon):
    assert P2(0.5, 0.5) == cw_polygon.centroid()
    assert P2(1.5, 1.5) == cw_polygon.translate(V2(1, 1)).centroid()
    assert P2(0.5, 0.5) == ccw_polygon.centroid()
    assert P2(1.5, 1.5) == ccw_polygon.translate(V2(1, 1)).centroid()


def test_polygon_centered_at(cw_polygon, ccw_polygon):
    assert P2(10, 10) == cw_polygon.centered_at(P2(10, 10)).centroid()

    assert P2(0, 0) == cw_polygon.centered_at(P2(0, 0)).centroid()
    assert P2(1, 1) == cw_polygon.centered_at(P2(1, 1)).centroid()
    assert P2(0, 0) == ccw_polygon.centered_at(P2(0, 0)).centroid()
    assert P2(1, 1) == ccw_polygon.centered_at(P2(1, 1)).centroid()


def test_polygon_rotate(cw_polygon):
    rotated = cw_polygon.rotate(math.pi / 2, P2(0, 0))
    expected = ApproxSet({P2(0.0, 0.0), P2(0.0, 1.0), P2(-1.0, 1.0), P2(-1.0, 0.0)})
    assert expected == rotated.points()


def test_polygon_perimiter(cw_polygon):
    assert 4 == cw_polygon.perimeter()


def test_polygon_simple(ccw_polygon, cw_polygon, cw_concave):
    assert ccw_polygon.is_simple()
    assert cw_polygon.is_simple()
    assert cw_concave.is_simple()


def test_intersecting(ccw_intersecting, cw_intersecting):
    assert not ccw_intersecting.is_simple()
    assert not cw_intersecting.is_simple()


def test_ccw_polygon_contains(ccw_polygon):
    assert ccw_polygon.contains(P2(0.5, 0.5))
    assert not ccw_polygon.contains(P2(2, 2))
    assert not ccw_polygon.contains(P2(-1, -1))


def test_cw_polygon_contains(cw_polygon):
    assert cw_polygon.contains(P2(0.5, 0.5))
    assert not cw_polygon.contains(P2(2, 2))
    assert not cw_polygon.contains(P2(-1, -1))

    assert cw_polygon.contains(P2(0.00001, 0.00001))
    assert cw_polygon.contains(P2(0.99999, 0.00001))
    assert cw_polygon.contains(P2(0.99999, 0.99999))
    assert cw_polygon.contains(P2(0.00001, 0.99999))

    assert cw_polygon.contains(P2(0, 0))
    assert cw_polygon.contains(P2(1, 0))
    assert cw_polygon.contains(P2(1, 1))
    assert cw_polygon.contains(P2(0, 1))

    assert cw_polygon.contains(P2(0.5, 0))
    assert cw_polygon.contains(P2(1, 0.5))
    assert cw_polygon.contains(P2(0.5, 1))
    assert cw_polygon.contains(P2(0, 0.5))

    assert not cw_polygon.contains(P2(-0.00001, -0.00001))
    assert not cw_polygon.contains(P2(1.00001, -0.00001))
    assert not cw_polygon.contains(P2(1.00001, 1.00001))
    assert not cw_polygon.contains(P2(-0.00001, 1.00001))

    assert not cw_polygon.contains(P2(-0.0001, 0))
    assert not cw_polygon.contains(P2(0, -0.00001))
    assert not cw_polygon.contains(P2(1.00001, 0))
    assert not cw_polygon.contains(P2(1, -0.00001))


def test_ccw_polygon_centroid(ccw_polygon):
    assert ccw_polygon.centroid() == P2(0.5, 0.5)


def test_cw_polygon_centroid(cw_polygon):
    assert cw_polygon.centroid() == P2(0.5, 0.5)


def test_cw_area(cw_polygon):
    assert cw_polygon.area() == 1


def test_ccw_area(ccw_polygon):
    assert ccw_polygon.area() == 1


def test_jarvis_convex_hull():
    points = [P2(0, 3), P2(2, 2), P2(1, 1), P2(2, 1), P2(3, 0), P2(0, 0), P2(3, 3)]
    points = sorted(points, key=lambda p: p._coords)
    expected = [P2(0, 0), P2(3, 0), P2(3, 3), P2(0, 3)]
    for a, e in zip(_jarvis_convex_hull(points), expected):
        assert a == e


def test_convex_hull(hull_data):
    (point_cloud, hull) = hull_data

    # test_hull = _standard_form(convex_hull(point_cloud))
    # data_hull = _standard_form(hull)

    assert Polygon(hull) == Polygon.ConvexHull(point_cloud)

    # for a, e in zip(test_hull, data_hull):
    #    assert a == e

    # hull_poly = Polygon.ConvexHull(point_cloud)
    # for e, a in zip(data_hull, hull_poly.points()):
    #    assert a == e


def test_is_convex(cw_polygon, ccw_polygon, cw_intersecting, cw_concave):
    assert cw_polygon.is_convex()
    assert ccw_polygon.is_convex()
    assert not cw_intersecting.is_convex()
    assert not cw_concave.is_convex()


def est_convex_hull():
    left = [P2(0, 0), P2(10, -1), P2(11, 3)]
