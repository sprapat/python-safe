class Card:
    SCORE = {'A': 11, 'J': 10, 'Q': 10, 'K': 10}

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        if value in 'AJQK':
            self.score = Card.SCORE[self.value]
        else:
            self.score = int(self.value)

    def get_score(self):
        return self.score

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def __eq__(self, other):
        return (other != None) and (self.value == other. get_value()) and \
            (self.suit == other.get_suit()) 