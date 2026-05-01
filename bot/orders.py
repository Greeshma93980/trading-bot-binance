import time
import hmac
import hashlib
import requests
import os
from urllib.parse import urlencode

BASE_URL = "https://testnet.binancefuture.com"

def place_order(symbol, side, order_type, quantity, price=None):
    api_key = os.getenv("BINANCE_API_KEY")
    secret = os.getenv("BINANCE_API_SECRET")

    endpoint = "/fapi/v1/order"

    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "timestamp": int(time.time() * 1000)
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    query_string = urlencode(params)
    
    signature = hmac.new(
        secret.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()

    params["signature"] = signature

    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.post(
        BASE_URL + endpoint,
        headers=headers,
        params=params
    )

    return response.json()