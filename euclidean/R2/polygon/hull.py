from euclidean.R2.space import P2

def convex_hull(points):
    if len(points) < 3:
        return None
    points = sorted(points, key=lambda p: p._coords)
    return _jarvis_convex_hull(points)

def _jarvis_convex_hull(points):
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