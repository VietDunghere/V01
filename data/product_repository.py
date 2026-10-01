"""Read product records from the local JSON dataset."""

import json
from pathlib import Path


class ProductRepository:
    def __init__(self, path=None):
        dataset_path = Path(path) if path else Path(__file__).resolve().parents[1] / "dataset" / "products.json"
        with dataset_path.open(encoding="utf-8") as file:
            self._products = json.load(file)

    def all_products(self):
        """Return all product records."""
        return list(self._products)

    def find_by_id(self, product_id):
        """Return a product by ID, or None."""
        return next((product for product in self._products if product["id"] == product_id), None)
