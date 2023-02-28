import unittest
from lognormal import Lognormal

class TestLognormal(unittest.TestCase):
    def setUp(self):
        self.dist = Lognormal(10, 20)
    
    def test_parameters(self):
        self.assertAlmostEqual(self.dist.mu, 2.1269280110429723)
        self.assertAlmostEqual(self.dist.sigma, 0.4606755615091099)
    
    def test_draw(self):
        samples = self.dist.draw(n=1000)
        self.assertEqual(len(samples), 1000)
        self.assertTrue(all(isinstance(x, float) for x in samples))
        self.assertTrue(all(x >= 0 for x in samples))
    
    def test_draw_ppf(self):
        percentiles = [0.1, 0.2, 0.3, 0.4, 0.5]
        samples = self.dist.draw_ppf(percentiles)
        self.assertEqual(len(samples), 5)
        self.assertTrue(all(isinstance(x, float) for x in samples))
        self.assertTrue(all(x >= 0 for x in samples))
    
    def test_mean(self):
        self.assertAlmostEqual(self.dist.mean(), 14.677992676873792)
        self.assertAlmostEqual(self.dist.mean(round_to=1), 14.7)

if __name__ == '__main__':
    unittest.main()