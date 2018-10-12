from multipledispatch import dispatch

from euclidean.constants import tau

from euclidean.R2.cartesian import V2
from euclidean.R2.line import LineSegment
from euclidean.R2.circle import Circle
from euclidean.R2.polygon import Polygon


@dispatch(LineSegment)
def rasterize(line_segment, n=100):
    step_vec = line_segment.vector() / n
    return [line_segment._p1 + i * step_vec for i in range(n)]


@dispatch(Circle)
def rasterize(circle, n=360):
    rot_theta = tau / n
    radius_vector = circle.radius * V2(1, 0)
    return [circle.center + radius_vector.rotate(rot_theta * i) for i in range(n)]


@dispatch(Polygon)
def rasterize(polygon, n=1000):
    raster = []
    n_per_edge = n // len(polygon)
    for edge in polygon.edges():
        raster.extend(rasterize(edge, n_per_edge))
    return raster
