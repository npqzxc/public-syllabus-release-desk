import unittest

from app.db import get_session
from app.services.contract_service import get_contract_detail
from app.services.dashboard_service import build_dashboard
from app.services.vendor_service import get_vendor_detail, list_vendors
from tests.test_helpers import build_test_app


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir, self.app = build_test_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.session = get_session()

    def tearDown(self):
        self.session.close()
        self.ctx.pop()
        self.temp_dir.cleanup()

    def test_dashboard_has_seed_metrics(self):
        payload = build_dashboard(self.session)
        self.assertGreaterEqual(payload["vendor_total"], 4)
        self.assertGreaterEqual(payload["open_risks"], 1)

    def test_vendor_filter_and_detail(self):
        payload = list_vendors(self.session, {"status": "risk"})
        self.assertEqual(payload["filters"]["status"], "risk")
        self.assertTrue(payload["items"])

        detail = get_vendor_detail(self.session, "LATTICE")
        self.assertIsNotNone(detail)
        self.assertEqual(detail["code"], "LATTICE")

    def test_contract_detail_contains_risks(self):
        detail = get_contract_detail(self.session, 4)
        self.assertIsNotNone(detail)
        self.assertTrue(detail["risks"])


if __name__ == "__main__":
    unittest.main()
