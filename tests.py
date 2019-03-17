import unittest

from server import app

class ProTagTests(unittest.TestCase):
    """Tests for ProTag."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"ProTag", result.data)

    def test_network(self):
        result = self.client.get("/network")
        self.assertIn(b"Thanks", result.data)

    def test_network_name(self):
        result = self.client.get("/network")
        self.assertNotIn(b"Ryan Barner, Full-Stack Engineer", result.data)

    def test_resume(self):
        result = self.client.get("/resume")
        self.assertIn(b"Ryan Barner, Full-Stack Engineer", result.data)

if __name__ == "__main__":
    unittest.main()