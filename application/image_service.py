"""Validate an artificial image feature vector."""

import numpy as np


class ImageService:
    def encode(self, image_input):
        """Convert a simulated image input to a finite, nonzero 4D vector."""
        try:
            embedding = np.asarray(image_input, dtype=float)
        except (TypeError, ValueError) as error:
            raise ValueError("Image vector must contain numeric values.") from error
        if embedding.ndim != 1 or embedding.size != 4 or not np.all(np.isfinite(embedding)):
            raise ValueError("Image vector must have four finite numeric values.")
        if np.linalg.norm(embedding) == 0:
            raise ValueError("Image vector must not be all zeros.")
        return embedding
