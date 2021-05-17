from .Hand import Hand
from collections import deque


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.hands = []
        self.queue = None
        self.counter = 1
        self.a_hand = None

    def get_name(self):
        return self.name

    def create_hand(self, display):
        self.a_hand = Hand(self, display)
        self.hands.append(self.a_hand)
        return self.a_hand

    def get_hand(self):
        for hand in self.hands:
            return hand

    def get_all_hands(self):
        return self.hands

    def add_hand_to_play_queue(self, hand):
        self.queue.appendleft(hand)

    def play(self, deck, game):
        self.queue = deque(self.hands)
        while len(self.queue) > 0:
            hand = self.queue.popleft()
            hand.play(deck, game)

    def show_all_players(self, game):
        for player in game.players:
            for hand in player.hands:
                hand.show_player()

    def __eq__(self, other):
        return (other != None) and (self.name == other.get_name())