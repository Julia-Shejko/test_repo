import json

import requests
from django.conf import settings
from django.http import JsonResponse

from exchange_rates.services import AlphavantageResponse


def convert(request):
    request_body = json.loads(request.body)
    from_currency = request_body["from"]
    to_currency = request_body["to"]
    url = (
        f"{settings.ALPHA_VANTAGE_BASE_URL}/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    )
    response = requests.get(url)
    alphavantage_response = AlphavantageResponse(**response.json())
    return JsonResponse(alphavantage_response.dict())
