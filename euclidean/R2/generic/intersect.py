from multipledispatch import dispatch

from euclidean.R2.line import Line, LineSegment
from euclidean.R2.circle import Circle
from euclidean.R2.polygon import Polygon
from euclidean.R2.cartesian import P2, V2


@dispatch(Line, Line)
def intersect(line_1, line_2):
    point = line_1.intersection(line_2)
    return {point} if point else set()


@dispatch(LineSegment, LineSegment)
def intersect(line_segment_1, line_segment_2):
    point = line_segment_1.intersection(line_segment_2)
    return {point} if point else set()


@dispatch(Line, LineSegment)
def intersect(line, line_segment):
    return line_line_segment_intersection(line, line_segment)


@dispatch(LineSegment, Line)
def intersect(line_segment, line):
    return line_line_segment_intersection(line, line_segment)


@dispatch(Line, Circle)
def intersect(line, circle):
    return line_circle_intersection(line, circle)


@dispatch(Circle, Line)
def intersect(circle, line):
    return line_circle_intersection(line, circle)


@dispatch(LineSegment, Circle)
def intersect(line_segment, circle):
    return line_segment_circle_intersection(line_segment, circle)


@dispatch(Circle, LineSegment)
def intersect(circle, line_segment):
    return line_segment_circle_intersection(line_segment, circle)


@dispatch(Circle, Circle)
def intersect(circle_1, circle_2):
    return circle_circle_intersection(circle_1, circle_2)


@dispatch(Polygon, Line)
def intersect(polygon, line):
    return polygon_intersection(polygon, line)


@dispatch(Line, Polygon)
def intersect(line, polygon):
    return polygon_intersection(polygon, line)


@dispatch(Polygon, LineSegment)
def intersect(polygon, line_segment):
    return polygon_intersection(polygon, line_segment)


@dispatch(LineSegment, Polygon)
def intersect(line_segment, polygon):
    return polygon_intersection(polygon, line_segment)


@dispatch(Polygon, Circle)
def intersect(polygon, circle):
    raise NotImplementedError("todo")


@dispatch(Circle, Polygon)
def intersect(circle, polygon):
    raise NotImplementedError("todo")


# implementations


def line_line_segment_intersection(line, line_segment):
    point = line.intersection(line_segment.line())
    if line_segment.contains(point):
        return {point}
    return set()


def line_circle_intersection(line, circle):
    vector = circle.center.vector()
    line = line.translate(-vector)
    if line._cy == 0:
        p1 = P2(line.x(0), 0)
        p2 = P2(line.x(1), 1)
    else:
        p1 = P2(0, line.y(0))
        p2 = P2(1, line.y(1))

    dv = p2 - p1
    dr2 = dv.magnitude() ** 2
    determinant = p1.x * p2.y - p1.y * p2.x
    discriminant = circle.radius ** 2 * dr2 - determinant ** 2
    if discriminant < 0:
        return set()

    x0 = determinant * dv.y / dr2
    y0 = -determinant * dv.x / dr2

    central = P2(x0, y0) + vector

    if discriminant == 0:
        return {central}

    sqrt_descriminant = discriminant ** 0.5
    sign_y = -1 if dv.y < 0 else 1
    x_off = sign_y * dv.x * sqrt_descriminant / dr2
    y_off = abs(dv.y) * sqrt_descriminant / dr2
    offset = V2(x_off, y_off)

    return {central + offset, central - offset}


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
