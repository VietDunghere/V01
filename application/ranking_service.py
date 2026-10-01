"""Assign final ranking scores and order candidates."""

import math


class RankingService:
    def rank_text(self, candidates):
        return self._rank(candidates, lambda item: item["text_score"])

    def rank_image(self, candidates):
        return self._rank(candidates, lambda item: item["image_score"])

    def rank_multimodal(self, candidates, text_weight=0.5, image_weight=0.5):
        if (not math.isfinite(text_weight) or not math.isfinite(image_weight)
                or text_weight < 0 or image_weight < 0
                or not math.isclose(text_weight + image_weight, 1.0)):
            raise ValueError("Text and image weights must be nonnegative and sum to 1.")
        return self._rank(
            candidates,
            lambda item: text_weight * item["text_score"] + image_weight * item["image_score"],
            combined=True,
        )

    def _rank(self, candidates, score_for, combined=False):
        results = []
        for candidate in candidates:
            result = dict(candidate)
            result["ranking_score"] = score_for(candidate)
            if combined:
                result["combined_score"] = result["ranking_score"]
            results.append(result)
        return sorted(results, key=lambda item: item["ranking_score"], reverse=True)
