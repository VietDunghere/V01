"""Artificial product feature vectors for the image search simulation."""

import numpy as np


class VectorIndex:
    def __init__(self):
        # Dimensions: footwear, bags, apparel, accessories/electronics.
        self._embeddings = {
            1: np.array([0.95, 0.05, 0.00, 0.00]),
            2: np.array([0.82, 0.12, 0.06, 0.00]),
            3: np.array([0.90, 0.08, 0.02, 0.00]),
            4: np.array([0.05, 0.95, 0.00, 0.00]),
            5: np.array([0.10, 0.90, 0.00, 0.00]),
            6: np.array([0.00, 0.00, 0.95, 0.05]),
            7: np.array([0.00, 0.00, 0.90, 0.10]),
            8: np.array([0.00, 0.00, 0.08, 0.92]),
            9: np.array([0.00, 0.00, 0.05, 0.95]),
            10: np.array([0.88, 0.08, 0.04, 0.00]),
        }

    def all_embeddings(self):
        """Return product ID to embedding pairs."""
        return self._embeddings.items()

    def get_embedding(self, product_id):
        """Return an embedding by product ID, or None."""
        return self._embeddings.get(product_id)
