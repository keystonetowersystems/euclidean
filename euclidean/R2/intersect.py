from multipledispatch import dispatch

from .line import Line, LineSegment
from .circle import Circle
from .polygon import Polygon
from .space import P2

@dispatch(Line, Line)
def intersect(line_1, line_2):
    return line_1.intersect(line_2)

@dispatch(LineSegment, LineSegment)
def intersect(line_segment_1, line_segment_2):
    return line_segment_1.intersection(line_segment_2)

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
    pass

@dispatch(Circle, Polygon)
def intersect(circle, polygon):
    pass

# implementations


def line_line_segment_intersection(line, line_segment):
    point = line.intersection(line_segment.line())
    if point in line_segment:
        return point
    return None

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
    x0 = determinant * dv.y / dr2
    y0 = -determinant * dv.x / dr2
    if discriminant <= 0:
        return (P2(x0, y0) + vector, )

    sqrt_descriminant = discriminant ** 0.5
    sign_y = 1 if dv.y > 0 else 0 if dv.y == 0 else -1
    x_off = sign_y * dv.x * sqrt_descriminant / dr2
    y_off = abs(dv.y) * sqrt_descriminant / dr2

    return (P2(x0 + x_off, y0 + y_off) + vector, P2(x0 - x_off, y0 - y_off) + vector)


def line_segment_circle_intersection(line_segment, circle):
    points = intersect(line_segment.line(), circle)
    return tuple(p for p in points if p in line_segment)

def circle_circle_intersection(circle_1, circle_2):
    return circle_1.intersection(circle_2)

def polygon_intersection(polygon, other):
    points = []

    for edge in polygon.edges():
        edge_result = intersect(edge, other)
        if edge_result is not None:
            points.append(edge_result)

    return points