from fuzzyfloat import rel_fp

from euclidean.util import normalize_coefficients, wrap_args

from .space import P3, V3


class Plane:

    @staticmethod
    def PointNormal(point, normal_vector):
        pass

    def __init__(self, cx, cy, cz, c, c_type=rel_fp):
        self._coeffs = wrap_args(c_type, *normalize_coefficients(cx, cy, cz, c))


