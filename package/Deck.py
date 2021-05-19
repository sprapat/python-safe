import random
from .Card import Card


class Deck:
    def __init__(self):
        value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
        suit = ['C', 'H', 'S', 'D']
        self.cards = [Card(v, s) for v in value for s in suit]
        # keep list of drawn cards
        self.drawn = []
    
    def get_deck(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)     

    def get_deck_left(self):
        return len(self.cards)

    def draw(self, number_of_cards):
        if self.cards:
            draw = [self.cards.pop(0) for c in range(number_of_cards)]
            self.drawn.extend(draw)
            return draw
        return [] 

    def update_count(self):
        return sum([card.get_count() for card in self.drawn])
        