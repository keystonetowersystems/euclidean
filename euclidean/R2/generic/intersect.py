from multipledispatch import dispatch

from euclidean.R2.line import Line, LineSegment
from euclidean.R2.circle import Circle
from euclidean.R2.polygon import Polygon
from euclidean.R2.cartesian import P2, V2


@dispatch(Line, Line)
def intersect(line_1, line_2):
    point = line_1.intersection(line_2)
    return {point} if point else set()


@intersect.register(LineSegment, LineSegment)
def _(line_segment_1, line_segment_2):
    point = line_segment_1.intersection(line_segment_2)
    return {point} if point else set()


@intersect.register(Line, LineSegment)
def _(line, line_segment):
    return line_line_segment_intersection(line, line_segment)


@intersect.register(LineSegment, Line)
def _(line_segment, line):
    return line_line_segment_intersection(line, line_segment)


@intersect.register(Line, Circle)
def _(line, circle):
    return line_circle_intersection(line, circle)


@intersect.register(Circle, Line)
def _(circle, line):
    return line_circle_intersection(line, circle)


@intersect.register(LineSegment, Circle)
def _(line_segment, circle):
    return line_segment_circle_intersection(line_segment, circle)


@intersect.register(Circle, LineSegment)
def _(circle, line_segment):
    return line_segment_circle_intersection(line_segment, circle)


@intersect.register(Circle, Circle)
def _(circle_1, circle_2):
    return circle_circle_intersection(circle_1, circle_2)


@intersect.register(Polygon, Line)
def _(polygon, line):
    return polygon_intersection(polygon, line)


@intersect.register(Line, Polygon)
def _(line, polygon):
    return polygon_intersection(polygon, line)


@intersect.register(Polygon, LineSegment)
def _(polygon, line_segment):
    return polygon_intersection(polygon, line_segment)


@intersect.register(LineSegment, Polygon)
def _(line_segment, polygon):
    return polygon_intersection(polygon, line_segment)


@intersect.register(Polygon, Circle)
def _(polygon, circle):
    raise NotImplementedError("todo")


@intersect.register(Circle, Polygon)
def _(circle, polygon):
    raise NotImplementedError("todo")


# implementations


def line_line_segment_intersection(line, line_segment):
    point = line.intersection(line_segment.line())
    if line_segment.contains(point):
        return {point}
    return set()


def line_circle_intersection(line, circle):
    vcenter = circle.center.vector()
    line = line.translate(-vcenter)

    p0 = line.closest(P2(0, 0))
    d0 = p0.vector().magnitude()

    if d0 == circle.radius:
        return set([p0 + vcenter])
    elif d0 > circle.radius:
        return set()
    else:
        a = line._cx**2 + line._cy**2
        d = circle.radius**2 - line._c**2 / a
        mult = (d / a)**0.5
        i1 = P2(p0.x + line._cy * mult, p0.y - line._cx * mult)
        i2 = P2(p0.x - line._cy * mult, p0.y + line._cx * mult)
        return set([i1 + vcenter, i2 + vcenter])


def line_segment_circle_intersection(line_segment, circle):
    points = intersect(line_segment.line(), circle)
    return set(p for p in points if line_segment.contains(p))


def circle_circle_intersection(circle_1, circle_2):
    return circle_1.intersection(circle_2)


def polygon_intersection(polygon, other):
    points = set()

    for edge in polygon.edges():
        points = points | intersect(edge, other)

    return points
