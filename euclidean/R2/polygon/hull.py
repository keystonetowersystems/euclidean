from euclidean.R2.space import P2


def convex_hull(points):
    if len(points) < 3:
        return None
    points = sorted(points, key=lambda p: p._coords)
    return _jarvis_convex_hull(points)


def _jarvis_convex_hull(points):
    """Find the convex hull of a point cloud using the jarvis march algorithm.

    Notes:

        O(n * h) for n points in point cloud, h points in hull

    Args:
        points (List[P2]):

    Returns:
        (List[P2]):
    """
    count = len(points)
    hull = []
    last_idx = 0
    while True:
        hull.append(points[last_idx])

        next_idx = (last_idx + 1) % count
        for test_idx, test_point in enumerate(points):
            if P2.CCW(points[last_idx], test_point, points[next_idx]) > 0:
                next_idx = test_idx

        last_idx = next_idx

        if last_idx == 0:
            return hull


def _divide_and_conquer_convex_hull(points):
    """

    Notes:

        O(n * log(n))

    Args:
        points:

    Returns:

    """
    count = len(points)
    if count < 6:
        return _jarvis_convex_hull(points)

    midpoint = count // 2
    min_cloud, max_cloud = points[:midpoint], points[midpoint:]

    min_hull = _divide_and_conquer_convex_hull(min_cloud)
    max_hull = _divide_and_conquer_convex_hull(max_cloud)

    return _merge_convex_hulls(min_hull, max_hull)


def _merge_convex_hulls(left_hull, right_hull):
    pass


def _min_tangent(min_hull, max_hull):
    pass


def _max_tangent(min_hull, max_hull):
    pass
