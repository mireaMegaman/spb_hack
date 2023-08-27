import numpy as np
from numpy.linalg import norm
from typing import List
from numba import njit
import pandas as pd


def encode_one_record(
        address,
        model
):
    """
    :param address: str, user's address
    :param model: SentenceTransformer, s-bert model
    :return: embedding of address
    """
    sentence_embeddings = list(model.encode([address]))
    return sentence_embeddings[0]


@njit
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


def predict(
        embedding
):

    ts = pd.read_csv('spb_hack\check_address\ML\\building.csv')
    idx = ts['id']
    with open('spb_hack\\check_address\\ML\\embeddings.npy', 'rb') as f:
        np_test_embs = np.load(f)

    max_sim = -1
    label = -1
    for i in range(len(np_test_embs)):
        sim = cosine_similarity(embedding, np_test_embs[i, :])
        if sim > max_sim:
            max_sim = sim
            label = idx[i]
    predicted_address = list(ts[ts['id'] == label]['full_address'])
    return label, predicted_address, max_sim