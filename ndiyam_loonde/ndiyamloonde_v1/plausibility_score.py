
from typing import Dict

import numpy as np

def get_score(text:str,
              model):
    text = text.lower()
    score = 0
    N = len(text)
    for i in range(len(text)-1):
        pair = (text[i], text[i+1])

        if pair in model:
            score += np.log(model[pair])
        else:
            score += np.log(1e-8)  

    return score / max(N,1)