"""
Service for calculating mathematical cosine similarity between two embedding vectors.
"""

from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityService:
    """
    Handles similarity computations between embedding vectors.
    
    Provides standard conversions from distance metrics to readable percentage match scores.
    """

    @staticmethod
    def calculate_cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
        """
        Calculates the cosine similarity between two vectors and maps it to a 0-100 scale.

        Args:
            vector_a (List[float]): First vector embedding (e.g., resume).
            vector_b (List[float]): Second vector embedding (e.g., job description).

        Returns:
            float: A matching score percentage between 0.0 and 100.0.

        Raises:
            ValueError: If vectors differ in dimensionality or are empty.
        """
        if not vector_a or not vector_b:
            raise ValueError("Input vectors cannot be empty.")
            
        if len(vector_a) != len(vector_b):
            raise ValueError(
                f"Vector dimension mismatch: vector_a ({len(vector_a)}) "
                f"does not match vector_b ({len(vector_b)})."
            )

        # Convert lists to 2D numpy arrays as required by scikit-learn
        array_a = np.array(vector_a).reshape(1, -1)
        array_b = np.array(vector_b).reshape(1, -1)

        # Calculate cosine similarity: returns matrix of shape (1, 1)
        similarity_val = float(cosine_similarity(array_a, array_b)[0][0])

        # Clamp similarity to [0.0, 1.0] range (negative similarity makes no sense for resume matching)
        clamped_score = max(0.0, min(1.0, similarity_val))

        # Scale to 0-100
        return clamped_score * 100.0
