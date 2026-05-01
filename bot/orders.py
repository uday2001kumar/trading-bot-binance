import time
from bot.logging_config import setup_logger

logger = setup_logger()


class OrderService:
    def __init__(self, client):
        self._client = client

    def place_order(self, validated: dict) -> dict:
        params = {
            "symbol": validated["symbol"],
            "side": validated["side"],
            "type": validated["type"],
            "quantity": validated["quantity"],
        }

        if validated["type"] == "LIMIT":
            params["price"] = validated["price"]
            params["timeInForce"] = "GTC"

        logger.info("Placing order: %s", params)

        response = self._client.new_order(**params)
        order_id = response.get("orderId")

        return self._wait_for_execution(validated["symbol"], order_id)

    def _wait_for_execution(self, symbol, order_id):
        for _ in range(5):
            time.sleep(1)
            order = self._client.get_order(symbol, order_id)

            if order.get("status") in ["FILLED", "PARTIALLY_FILLED"]:
                return order

        return order