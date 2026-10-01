"""Read order records from the local JSON dataset."""

import json
from pathlib import Path


class OrderRepository:
    def __init__(self, path=None):
        dataset_path = Path(path) if path else Path(__file__).resolve().parents[1] / "dataset" / "orders.json"
        with dataset_path.open(encoding="utf-8") as file:
            self._orders = json.load(file)

    def find_order(self, order_id):
        """Return an order by ID, or None."""
        return next((order for order in self._orders if order["order_id"] == order_id), None)
