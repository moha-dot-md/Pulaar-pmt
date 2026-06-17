class State:

    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.expectation = -0.0111

    def is_final(self):
        return True if self.score/len(self.text) >= self.expectation else False
