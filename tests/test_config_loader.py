import unittest
from backend.config.settings import Settings

class TestConfigLoader(unittest.TestCase):

    def test_settings_loader(self):
        s = Settings()
        val = s.validate_settings()
        self.assertIn("valid", val)
        self.assertIn("environment", val)
        self.assertTrue(s.DATABASE_URL)
        self.assertTrue(s.JWT_SECRET_KEY)

if __name__ == "__main__":
    unittest.main()
