

from ndiyamloonde_v1.ndiyamloonde_bigramme import normalize_text
from collections import defaultdict
import numpy as np



def get_prob_ngram(text, n=3):
    text = normalize_text(text)
    counts = defaultdict(int)
    totals = defaultdict(int)
    vocab = set()

    for i in range(len(text) - (n - 1)):
        gram = text[i : i + n]
        prefix = gram[:-1]
        counts[gram] += 1
        totals[prefix] += 1
        for c in gram:
            vocab.add(c)

    V = len(vocab)
    probs = {}
    for gram, c in counts.items():
        prefix = gram[:-1]
        probs[gram] = (c + 1) / (totals[prefix] + V)

    return probs


def get_score_ngram(text, model, n=3):
    text = normalize_text(text)
    score = 0.0
    count = 0
    for i in range(len(text) - (n - 1)):
        gram = text[i : i + n]
        prob = model.get(gram, 1e-8)
        score += np.log(prob)
        count += 1
    return score / max(count, 1)
