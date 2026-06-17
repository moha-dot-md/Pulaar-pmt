

from heapq import nlargest
from itertools import product
from ndiyamloonde_v1.ndiyamloonde_bigramme import SUBSTITUTIONS, normalize_text
from .n_gram import get_score_ngram

def generate_possible_substitutions_by_word(text: str, model, n=3):

    text = normalize_text(text)

    options = []

    for char in text:

        if char in SUBSTITUTIONS:

            if char == "n":
                options.append([char] + list(SUBSTITUTIONS[char]))
            else:
                options.append([char, SUBSTITUTIONS[char]])

        else:
            options.append([char])

    results = []

    for combo in product(*options):
        candidate = "".join(combo)
        score = get_score_ngram(candidate, model, n)
        results.append((candidate, score))

    best = nlargest(n, results, key=lambda x: x[1])

    return [x[0] for x in best]


def correct_word(word, model, n=3):
    candidates = generate_possible_substitutions_by_word(word, model, n)
    return max(candidates, key=lambda w: get_score_ngram(w, model, n))


def correct_text(text, model, n=3):
    words = text.split()
    return " ".join(correct_word(w, model, n) for w in words)
