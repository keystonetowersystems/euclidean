import unittest

from euclidean.constants import eta

from euclidean.R2.space import V2, P2

class V2TestCase(unittest.TestCase):

    def test_dot_product(self):
        v1 = V2(1, 0)
        v2 = V2(0, 1)
        self.assertEqual(v1.dot(v2), 0)
        self.assertEqual(v1.dot(v1), 1)
        self.assertEqual(v2.dot(v2), 1)

        v3 = V2(1, 1)
        self.assertEqual(v3.dot(v3), 2)

        v4 = V2(-2, -2)
        self.assertEqual(v4.dot(v4), 8)

    def test_cross_product(self):
        v1 = V2(1, 0)
        v2 = V2(0, 1)
        self.assertEqual(v1.cross(v2), 1)
        self.assertEqual(v2.cross(v1), -1)
        self.assertEqual(v1.cross(v1), 0)
        self.assertEqual(v2.cross(v2), 0)

        v3 = V2(1, 1)
        self.assertEqual(v3.cross(v1), -1)
        self.assertEqual(v1.cross(v3), 1)
        self.assertEqual(v3.cross(v2), 1)
        self.assertEqual(v2.cross(v3), -1)

    def test_add(self):
        v1 = V2(0, 0)
        v2 = V2(1, 0)
        v3 = V2(0, 1)

        self.assertEqual(v1 + v2 + v3, V2(1, 1))

        v1 += v2
        self.assertEqual(v1, V2(1, 0))

        v1 += v3
        self.assertEqual(v1, V2(1, 1))

    def test_sub(self):
        v1 = V2(100, 100)
        v2 = V2(25, 50)
        v3 = V2(0, 0)

        self.assertEqual(v1 - v2, V2(75, 50))
        self.assertEqual(v2 - v3, v2)

        v3 -= v1
        self.assertEqual(v3, V2(-100, -100))

    def test_mul(self):
        v1 = V2(1, 2)
        self.assertEqual(v1 * 2, V2(2, 4))

        v1 *= -3
        self.assertEqual(v1, V2(-3, -6))

    def test_div(self):
        v1 = V2(1, 2)
        self.assertEqual(v1 / 2, V2(0.5, 1))

        v1 /= -2
        self.assertEqual(v1, V2(-0.5, -1))

    def test_floordiv(self):
        v1 = V2(1, 2)
        self.assertEqual(v1 // 2, V2(0, 1))

        v1 //= 2
        self.assertEqual(v1, V2(0, 1))

    def test_angle(self):
        pass

    def test_parallel(self):
        pass

    def test_orthogonal(self):
        self.assertTrue(V2(1,0).is_orthogonal(V2(0,1)))
        self.assertTrue(V2(-1, -1).is_orthogonal(V2(-1, 1)))

        self.assertFalse(V2(1,0).is_orthogonal(V2(-1,0)))
        self.assertFalse(V2(1,1).is_orthogonal(V2(1, 0)))

    def test_rotate(self):
        v1 = V2(1, 0)
        v1 = v1.rotate(eta)
        self.assertAlmostEqual(v1.x, 0)
        self.assertAlmostEqual(v1.y, 1)

        v1 = v1.rotate(eta)
        self.assertAlmostEqual(v1.x, -1)
        self.assertAlmostEqual(v1.y, 0)

        v1 = v1.rotate(eta)
        self.assertAlmostEqual(v1.x, 0)
        self.assertAlmostEqual(v1.y, -1)

        v1 = v1.rotate(eta)
        self.assertAlmostEqual(v1.x, 1)
        self.assertAlmostEqual(v1.y, 0)

class P2TestCase(unittest.TestCase):
    pass