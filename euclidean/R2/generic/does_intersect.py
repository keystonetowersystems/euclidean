from multipledispatch import dispatch

from euclidean.R2.line import Line, LineSegment
from euclidean.R2.circle import Circle
from euclidean.R2.polygon import Polygon


@dispatch(Circle, Circle)
def does_intersect(circle1, circle2):
    return circle1.does_intersect(circle2)


@dispatch(Line, Line)
def does_intersect(line1, line2):
    return line1.does_intersect(line2)


@dispatch(LineSegment, LineSegment)
def does_intersect(line_segment1, line_segment2):
    return line_segment1.does_intersect(line_segment2)


@dispatch(Polygon, Polygon)
def does_intersect(polygon1, polygon2):
    # grab max and min points of polygons and return False if disjoint?

    for e1 in polygon1.edges():
        for e2 in polygon2.edges():
            if e1.does_intersect(e2):
                return True
    return False


@dispatch(Line, LineSegment)
def does_intersect(line, line_segment):
    return __does_intersect_line_line_segment(line, line_segment)


@dispatch(LineSegment, Line)
def does_intersect(line_segment, line):
    return __does_intersect_line_line_segment(line, line_segment)


@dispatch(Circle, Line)
def does_intersect(circle, line):
    return __does_intersect_circle_line(circle, line)


@dispatch(Line, Circle)
def does_intersect(line, circle):
    return __does_intersect_circle_line(circle, line)


@dispatch(Circle, LineSegment)
def does_intersect(circle, line_segment):
    return __does_intersect_circle_line_segment(circle, line_segment)


@dispatch(LineSegment, Circle)
def does_intersect(line_segment, circle):
    return __does_intersect_circle_line_segment(circle, line_segment)


@dispatch(Polygon, Line)
def does_intersect(polygon, line):
    return __does_intersect_polygon_line_like(polygon, line)


@dispatch(Line, Polygon)
def does_intersect(line, polygon):
    return __does_intersect_polygon_line_like(polygon, line)


@dispatch(Polygon, LineSegment)
def does_intersect(polygon, line_segment):
    return __does_intersect_polygon_line_like(polygon, line_segment)


@dispatch(LineSegment, Polygon)
def does_intersect(line_segment, polygon):
    return __does_intersect_polygon_line_like(polygon, line_segment)


def __does_intersect_circle_line(circle, line):
    eq = abs(line._equation(circle.center) - line._c)
    dist = eq / (line._cx ** 2 + line._cy ** 2) ** 0.5
    return dist <= circle.radius


def __does_intersect_circle_line_segment(circle, line_segment):
    closest = line_segment.line().closest(circle.center)
    p_min, p_max = line_segment.ordered()
    if closest > p_max:
        closest = p_max
    elif closest < p_min:
        closest = p_min

    dist_vec = circle.center - closest
    if dist_vec.dot(dist_vec) > circle.radius ** 2:
        return False
    return not circle.contains(p_min) or not circle.contains(p_max)


def __does_intersect_polygon_line_like(polygon, line):
    return any(does_intersect(line, edge) for edge in polygon.edges())


def __does_intersect_line_line_segment(line, line_segment):
    s1 = line.on_side(line_segment._p1)
    s2 = line.on_side(line_segment._p2)
    if s1 == 0 and s2 == 0:
        raise ValueError("Line Segment is a segment of Line.")
    return s1 != s2
