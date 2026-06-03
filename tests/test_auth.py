import unittest

from app.auth import hash_password


class AuthTests(unittest.TestCase):
    def test_hash_password_is_deterministic(self):
        self.assertEqual(hash_password("course123"), hash_password("course123"))
        self.assertNotEqual(hash_password("course123"), hash_password("vendor124"))


if __name__ == "__main__":
    unittest.main()
