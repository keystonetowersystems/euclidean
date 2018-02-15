import numpy as np

from collections import deque

from typing import List

from euclidean.options import epsilon
from euclidean.vector import Vector2

def orientation(a : Vector2, b : Vector2, c : Vector2) -> int:
    """
    Determine if the orientation of A->B->C is processing CW, CCW, or is colinear

    CW = -1
    colinear = 0
    CCW = 1

    :param a:
    :param b:
    :param c:
    :return:
    """

    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)

    if np.isclose(val, 0):
        return 0 # colinear

    return 1 if val > 0 else -1

def on_segment(a : Vector2, b : Vector2, c : Vector2) -> bool:
    """
    Does the point c fall on the line segment AB

    :param a:
    :param b:
    :param c:
    :return:
    """
    return min(a.x, c.x) <= b.x <= max(a.x, c.x) and min(a.y, c.y) <= b.y <= max(a.y, c.y)


def do_intersect(p1 : Vector2, q1 : Vector2, p2 : Vector2, q2 : Vector2) -> bool:
    """

    :param p1:
    :param q1:
    :param p2:
    :param q2:
    :return:
    """

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def is_simple_polygon(points : List[Vector2]) -> bool:
    min_y = min((p.y for p in points)) - 1
    max_y = max((p.y for p in points)) + 1

    segments = zip(points, points[1:])

    queue = deque(sorted(segments, key=lambda segment: (segment[0].x, segment[0].y)))
    #while queue:
    pass


