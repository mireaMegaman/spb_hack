from sentence_transformers import SentenceTransformer
from infer import encode_one_record, predict
from prepare_text import clean_text
import torch
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')


def seed_everything(seed):
    import random
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


if __name__ == '__main__':
    seed_everything(seed=42)

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    user_address = str(input()) # user input
    clean_data = clean_text(user_address)
    embedding = encode_one_record(clean_data, model)

    label, place, chance = predict(embedding)
    print(f'Predicted label is {label}, address is {place}, confidience: {chance}')






