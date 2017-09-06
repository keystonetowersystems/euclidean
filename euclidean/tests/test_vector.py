import unittest

from euclidean.vector import Vector2, Vector3

class TestVector2(unittest.TestCase):

    def test_translation(self):
        self.assertEqual(Vector2(1,1) + Vector2(1,1), Vector2(2,2))
        self.assertEqual(Vector2(1,1) - Vector2(1,1), Vector2(0,0))

        v = Vector2(1,1)

        v += Vector2(1,1)
        self.assertEqual(v, Vector2(2,2))

        v -= Vector2(2,2)
        self.assertEqual(v, Vector2(0, 0))

    def test_rotation(self):
        pass

    def test_scaling(self):
        self.assertEqual(Vector2(1,1) * 50, Vector2(50, 50))
        self.assertEqual(Vector2(50, 50) / 50, Vector2(1,1))

        v = Vector2(1, 1)
        v *= 50
        self.assertEquals(v, Vector2(50, 50))

        v /= 50
        self.assertEqual(v, Vector2(1,1))

if __name__ == '__main__':
    unittest.main()
