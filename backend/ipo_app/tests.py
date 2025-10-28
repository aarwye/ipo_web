from django.test import TestCase
from rest_framework.test import APIClient
from .models import IPO
from django.urls import reverse
from unittest.mock import patch

class IPOModelTest(TestCase):
    def setUp(self):
        self.ipo = IPO.objects.create(
            company_name="Test Company",
            price_band="100-120",
            open_date="2025-01-01",
            close_date="2025-01-05",
            issue_size="50 Cr",
            issue_type="Book Built",
            listing_date="2025-01-10",
            status="listed",
            ipo_price=110.00,
            listing_price=120.00,
            listing_gain="9%"
        )

    def test_ipo_str_method(self):
        """Check string representation"""
        self.assertEqual(str(self.ipo), "Test Company")

    def test_ipo_fields(self):
        """Ensure IPO fields are correctly saved"""
        self.assertEqual(self.ipo.status, "listed")
        self.assertEqual(self.ipo.price_band, "100-120")


class IPOAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ipo = IPO.objects.create(
            company_name="Local IPO",
            price_band="100-120",
            open_date="2025-01-01",
            close_date="2025-01-05",
            issue_size="10 Cr",
            issue_type="Fixed Price",
            listing_date="2025-01-10",
            status="listed",
        )

    def test_get_local_ipos(self):
        """Check /api/ipos/ endpoint"""
        response = self.client.get("/api/ipos/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Local IPO", str(response.data))

    @patch("ipo_app.views.finnhub.Client")
    def test_all_ipos_combined_endpoint(self, mock_client):
        """Check /api/all-ipos/ merges data correctly"""
        mock_client.return_value.ipo_calendar.return_value = {
            "ipoCalendar": [
                {
                    "date": "2025-08-19",
                    "exchange": "NASDAQ Global",
                    "name": "Mock IPO",
                    "numberOfShares": 5000000,
                    "price": "5.50-6.00",
                    "status": "filed",
                    "symbol": "MIPO",
                    "totalSharesValue": 25000000,
                }
            ]
        }

        response = self.client.get("/api/all-ipos/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock IPO", str(response.data))
        self.assertIn("Local IPO", str(response.data))
