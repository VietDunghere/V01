"""Generate candidates; final ordering belongs to RankingService."""

import numpy as np


def cosine_similarity(a, b):
    """Return cosine similarity, including a safe zero-vector result."""
    numerator = np.dot(a, b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


class SearchService:
    def __init__(self, product_repository, order_repository, vector_index):
        self.product_repository = product_repository
        self.order_repository = order_repository
        self.vector_index = vector_index

    def retrieve_text(self, query_text):
        """Match query words against product name, category, color and description."""
        if not isinstance(query_text, str) or not query_text.strip():
            raise ValueError("Text query must not be empty.")
        words = query_text.lower().strip().split()
        candidates = []
        for product in self.product_repository.all_products():
            searchable = " ".join(str(product[field]) for field in ("name", "category", "color", "description"))
            product_words = set(searchable.lower().split())
            score = sum(word in product_words for word in words) / len(words)
            if score > 0:
                candidates.append({"product": product, "text_score": score})
        return candidates

    def retrieve_image(self, query_embedding):
        """Compare a simulated query vector with all indexed products."""
        candidates = []
        for product in self.product_repository.all_products():
            embedding = self.vector_index.get_embedding(product["id"])
            if embedding is None:
                continue
            score = cosine_similarity(query_embedding, embedding)
            if score > 0:
                candidates.append({"product": product, "image_score": score})
        return candidates

    def retrieve_multimodal(self, query_text, query_embedding):
        """Join text and image candidates by product ID, preserving both scores."""
        by_id = {}
        for candidate in self.retrieve_text(query_text):
            product = candidate["product"]
            by_id[product["id"]] = {"product": product, "text_score": candidate["text_score"], "image_score": 0.0}
        for candidate in self.retrieve_image(query_embedding):
            product = candidate["product"]
            entry = by_id.setdefault(product["id"], {"product": product, "text_score": 0.0, "image_score": 0.0})
            entry["image_score"] = candidate["image_score"]
        return list(by_id.values())

    def find_order(self, order_id):
        """Look up an order by exact ID."""
        return self.order_repository.find_order(order_id)
