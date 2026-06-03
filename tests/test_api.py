import unittest

from tests.test_helpers import build_test_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir, self.app = build_test_app()
        self.client = self.app.test_client()
        self.client.post("/login", data={"username": "cora", "password": "course123"})

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dashboard_api(self):
        response = self.client.get("/api/dashboard")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("upcoming_contracts", payload)

    def test_vendor_api_filter(self):
        response = self.client.get("/api/vendors?status=review")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["filters"]["status"], "review")

    def test_contract_api_not_found(self):
        response = self.client.get("/api/contracts/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
