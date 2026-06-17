from collections import defaultdict
import unicodedata
import numpy as np
from heapq import nlargest

LOWER_CASE = {"Ɓ": "ɓ", "Ɗ": "ɗ", "Ƴ": "ƴ", "Ñ": "ñ", "Ŋ": "ŋ"}

SUBSTITUTIONS = {"b": "ɓ", "d": "ɗ", "y": "ƴ", "n": ("ñ", "ŋ")}



def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        text =  f.read()
    return unicodedata.normalize("NFC", text)


def normalize_text(text):

    text = unicodedata.normalize("NFC", text)

    normalized = ""

    for char in text:
        if (char.isalpha() or char==" ") and char in LOWER_CASE:
            normalized += LOWER_CASE[char]
        else:
            normalized += char.lower()

    return normalized


def get_prob(text):

    text = normalize_text(text)

    counts = defaultdict(int)
    totals = defaultdict(int)
    vocab = set()

    for i in range(len(text) - 1):

        a = text[i]
        b = text[i + 1]

        if (a.isalpha() or a == " ") and (b.isalpha() or b == " "):

            counts[(a, b)] += 1
            totals[a] += 1

            vocab.add(a)
            vocab.add(b)

    V = len(vocab)

    probs = {}

    for a in vocab:
        for b in vocab:

            probs[(a, b)] = (counts[(a, b)] + 1) / (totals[a] + V)

    return probs

def substitute_by_probabilty(text, model):
    text = normalize_text(text)
    result = text[0]
    for i in range(1, len(text)):
        prev = result[-1]
        char = text[i]
        if char in SUBSTITUTIONS:
            candidates = [char]
            if char == "n":
                candidates += list(SUBSTITUTIONS[char])
            else:
                candidates.append(SUBSTITUTIONS[char])
            best_char = char
            best_score = -1e9
            for c in candidates:
                prob = model.get((prev, c), 1e-8)
                if prob > best_score:
                    best_score = prob
                    best_char = c
            result += best_char
        else:
            result += char
    return result

def beam_search_substitution(text, model, beam_width=30):

    text = normalize_text(text)

    beam = [(text[0], 0)]

    for i in range(1, len(text)):

        new_beam = []
        char = text[i]

        for partial_text, score in beam:

            prev = partial_text[-1]

            if not (prev.isalpha() or prev == " "):
                prev = " "

            if char in SUBSTITUTIONS:

                candidates = [char]

                if char == "n":
                    candidates += list(SUBSTITUTIONS[char])
                else:
                    candidates.append(SUBSTITUTIONS[char])

            else:
                candidates = [char]

            for c in candidates:

                prob = model.get((prev, c), 1e-8)

                new_score = score + np.log(prob)

                new_beam.append((partial_text + c, new_score))

        beam = nlargest(beam_width, new_beam, key=lambda x: x[1])

    best_text, best_score = max(beam, key=lambda x: x[1])

    return best_text, best_score
