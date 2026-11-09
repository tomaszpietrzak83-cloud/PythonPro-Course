import unittest
from main import release


class GateTest(unittest.TestCase):
    def test_test_failure_stops_release(self):
        self.assertNotIn("staging", release(False, True, True))
