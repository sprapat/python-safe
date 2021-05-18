from .Hand import Hand
from collections import deque


class Player:
    """Class represent a player"""
    def __init__(self, player_name):
        self.name = player_name
        self.hands = []
        self.queue = None
        self.counter = 0

    def get_name(self):
        return self.name

    def get_counter(self):
        self.counter += 1
        return self.counter

    # Todo: I think create_hand method should not need display object
    def create_hand(self, display):
        a_hand = Hand(self, display)
        self.hands.append(a_hand)
        return a_hand

    # BUG: I think this is wrong because the method will always return the first hand, nothing else.
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

    # Todo: I think this method should be in game class because game class know all_players.
    def show_all_players(self, game):
        for player in game.players:
            for hand in player.hands:
                hand.show_player()

    def __eq__(self, other):
        return (other is not None) and (self.name == other.get_name())