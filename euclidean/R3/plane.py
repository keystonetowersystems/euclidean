from euclidean.util import normalize_coefficients

from .cartesian import P3, V3


class Plane:
    @staticmethod
    def PointNormal(point, normal_vector):
        pass

    def __init__(self, cx, cy, cz, c):
        self._coeffs = normalize_coefficients(cx, cy, cz, c)
