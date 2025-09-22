# Tests for metrics
import unittest
from models.resource import Resource
from metrics import ramp_up_time

class TestMetrics(unittest.TestCase):
    def test_ramp_up_time(self):
        res = Resource(name="test_model", category="MODEL")
        value, latency = ramp_up_time.compute(res)
        self.assertIsInstance(value, float)
        self.assertIsInstance(latency, int)

if __name__ == "__main__":
    unittest.main()
