# FINNHUB_API_KEY = 'd40c7apr01qqo3qh7ue0d40c7apr01qqo3qh7ueg'
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import IPO
from .serializers import IPOSerializer
import finnhub
import os
from dotenv import load_dotenv
load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
# --- 1. ViewSet for CRUD (for /api/ipos/) ---
class IPOViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer


# --- 2. Combined API (local + Finnhub live IPOs) ---
@api_view(['GET'])
def all_ipos(request):
    # Step 1: Get local IPOs (admin-uploaded)
    local_ipos = IPO.objects.all()
    local_data = IPOSerializer(local_ipos, many=True).data

    # Step 2: Get IPOs from Finnhub
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

    try:
        ipo_data = finnhub_client.ipo_calendar(_from="2025-01-01", to="2025-12-31")
        finnhub_ipos = ipo_data.get("ipoCalendar", [])
    except Exception as e:
        print("Error fetching Finnhub IPOs:", e)
        finnhub_ipos = []

    # Step 3: Map Finnhub data into your model’s structure
    external_data = []
    for item in finnhub_ipos:
        external_data.append({
            "company_name": item.get("name"),
            "price_band": item.get("price") or "N/A",
            "open_date": item.get("date"),
            "close_date": item.get("date"),  # Finnhub gives only one date
            "issue_size": item.get("numberOfShares") or "N/A",
            "issue_type": item.get("exchange") or "N/A",
            "listing_date": item.get("date"),
            "status": item.get("status") or "N/A",
            "ipo_price": None,
            "listing_price": None,
            "listing_gain": None
        })

    # Step 4: Combine local + external IPOs
    combined_data = local_data + external_data

    # Step 5: Return as JSON response
    return Response(combined_data)
