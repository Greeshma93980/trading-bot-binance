import typer
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger
from bot.client import get_client

app = typer.Typer()
logger = setup_logger()

@app.command()
def trade(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
):
    try:
        validate_order(symbol, side, order_type, quantity, price)

        logger.info(f"Order Request: {symbol} {side} {order_type} qty={quantity} price={price}")

        response = place_order(symbol, side, order_type, quantity, price)

        print("\n📦 RAW RESPONSE:")
        print(response)

        order_id = response.get("orderId")

        # Fetch final order details
        if order_id:
            client = get_client()
            details = client.futures_get_order(symbol=symbol, orderId=order_id)

            print("\n📊 FINAL ORDER DETAILS:")
            print(details)

            print("\n✅ ORDER SUMMARY")
            print(f"Order ID: {details.get('orderId')}")
            print(f"Status: {details.get('status')}")
            print(f"Executed Qty: {details.get('executedQty')}")
            print(f"Avg Price: {details.get('avgPrice')}")

            logger.info(f"Final Order: {details}")

        else:
            print("⚠️ No orderId returned")

    except Exception as e:
        print("\n❌ ORDER FAILED:", e)
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    app()