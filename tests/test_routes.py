import unittest

from tests.test_helpers import build_test_app


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir, self.app = build_test_app()
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def login(self):
        return self.client.post("/login", data={"username": "cora", "password": "course123"}, follow_redirects=False)

    def test_protected_route_redirects_to_login(self):
        response = self.client.get("/vendors")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_login_redirects_to_original_destination(self):
        self.client.get("/contracts/4")
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/contracts/4"))

    def test_contract_creation_flow(self):
        self.login()
        response = self.client.post(
            "/contracts",
            data={
                "vendor_id": "1",
                "title": "Incident Archive Extension",
                "status": "review",
                "annual_spend": "24000",
                "renewal_date": "2026-09-01",
                "sla_level": "silver",
                "procurement_stage": "legal_review",
            },
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/contracts/", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
