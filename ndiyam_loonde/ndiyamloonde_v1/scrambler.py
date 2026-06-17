import unicodedata

LOWER_CASE    = {"Ɓ": "ɓ", "Ɗ": "ɗ", "Ƴ": "ƴ", "Ñ": "ñ", "Ŋ": "ŋ"}
SUBSTITUTIONS = {"ɓ": "b", "ɗ": "d", "ƴ": "y", "ñ": "n", "ŋ": "n"}


def normalize_text(entry: str) -> str:
    text = unicodedata.normalize("NFC", entry)
    normalized = ""
    for char in text:
        if char in LOWER_CASE:
            normalized += LOWER_CASE[char]
        else:
            normalized += char.lower()
    return normalized


def scramble_word(word: str) -> str:
    return "".join(SUBSTITUTIONS.get(char, char) for char in word)


def scramble_text(entry: str) -> tuple[str, str]:
    """
    Substitutes every special character in the entire text.
    Returns:
        clean_text : normalized original
        noisy_text : fully substituted version
    """
    clean_text = normalize_text(entry)
    noisy_text = "".join(SUBSTITUTIONS.get(char, char) for char in clean_text)
    return clean_text, noisy_text


if __name__ == "__main__":
    sample = "ɓe ngol ɗon waɗa ŋaari, ɓe ngol ɗon waɗa ŋaariɓe ngol ɗon waɗa ŋaari, ɓe ngol ɗon waɗa ŋaari', ɓe ngol ɗon waɗa ŋaari"
    clean, noisy = scramble_text(sample)

    print("Clean :", clean)
    print("Noisy :", noisy)
    print("Identical:", clean == noisy)  # False means substitutions happened