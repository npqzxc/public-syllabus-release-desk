import unittest

from tests.test_helpers import build_test_app


class WebFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir, self.app = build_test_app()
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_login_redirects_back_to_original_page(self):
        initial = self.client.get("/contracts/4")
        self.assertEqual(initial.status_code, 302)
        self.assertIn("/login", initial.headers["Location"])

        login = self.client.post(
            "/login",
            data={"username": "cora", "password": "course123"},
            follow_redirects=False,
        )
        self.assertEqual(login.status_code, 302)
        self.assertTrue(login.headers["Location"].endswith("/contracts/4"))

    def test_contract_note_submission(self):
        self.client.post("/login", data={"username": "cora", "password": "course123"})
        response = self.client.post(
            "/contracts/1/notes",
            data={"note_type": "operations", "body": "Need procurement to confirm the fallback clause."},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("fallback clause", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
