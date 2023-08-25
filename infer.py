import numpy as np
from numpy.linalg import norm
from typing import List


def cosine_similarity(
        first_embedding: List[float],
        second_embedding: List[float]
) -> float:
    """
    :param first_embedding: List, user address's embeddings from model
    :param second_embedding: standart address's embeddings from database
    :return: float, embedding's similarity
    """
    return np.dot(first_embedding, second_embedding) \
           / (np.linalg.norm(first_embedding) * np.linalg.norm(second_embedding))
