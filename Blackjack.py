import curses
import random
from collections import deque
from time import sleep


class Display:
    SUIT_CHR = {'S': '\u2660', 'H': '\u2665', 'D': '\u2666', 'C': '\u2663'}

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.value = None
        self.suit = None

    def display_card_skeleton(self, y, x, symbol='#'):
        for a in range(6):
            self.stdscr.addstr(y, x + a, symbol)
            self.stdscr.addstr(y + 6, x + a, symbol)
        for b in range(7):
            self.stdscr.addstr(y + b, x, symbol)
            self.stdscr.addstr(y + b, x + 6, symbol)
        self.refresh()

    def display_card_symbol(self, y, x, value, suit):
        self.stdscr.addstr(y + 1, x + 1, value)
        self.stdscr.addstr(y + 1, x + 1 + len(str(value)), self.SUIT_CHR[suit])
        self.stdscr.addstr(y + 5, x + 5 - len(str(value)), value)
        self.stdscr.addstr(y + 5, x + 5, self.SUIT_CHR[suit])
        self.refresh()

    def clear_card_symbol(self, y, x, card_object):
        self.stdscr.addstr(y + 1, x + 1, ' ')
        self.stdscr.addstr(y + 1, x + 1 + len(str(card_object.get_value())), ' ')
        self.stdscr.addstr(y + 5, x + 5 - len(str(card_object.get_value())), ' ')
        self.stdscr.addstr(y + 5, x + 5, ' ')
        self.refresh()

    def display_decide(self, number, text, plus=0):
        self.stdscr.addstr(36 + plus, number * 18, text)
        self.refresh()

    def display_text_with_y(self, y, text):
        self.stdscr.addstr(y, 0, text)
        self.refresh()

    def display_text_times_seven(self, y, text):
        self.stdscr.addstr(y * 7, 0, text)
        self.refresh()

    def display_text(self, y, x, text, plusy=0, plusx=0):
        self.stdscr.addstr(y + plusy, x + plusx, text)
        self.refresh()

    def getstr(self, y, x):
        return self.stdscr.getstr(y, x)

    def refresh(self):
        self.stdscr.refresh()

    def display_card(self, y, x, card):
        value =card.get_value()
        suit = card.get_suit()
        self.display_card_skeleton(y * 7, x * 7)
        self.display_card_symbol(y * 7, x * 7, value, suit)
        self.refresh()

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

class Deck:
    def __init__(self):
        value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
        suit = ['C', 'H', 'S', 'D']
        self.cards = [Card(v, s) for v in value for s in suit]
    
    def get_deck(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, number_of_cards):
        return [self.cards.pop(0) for c in range(number_of_cards)]



class Hand:
    def __init__(self, player, display):
        self.cards = []
        self.player = player
        self.name = self.player.name
        self.card_count = 1
        self.display_object = display
        self.already_displayed = []

    def display_text(self, text1, text2, plus):
        self.display_text_formula('dealer', text1, text2, plus, 0)
        self.display_text_formula('player1', text1, text2, plus, 7)
        self.display_text_formula('sp1', text1, text2, plus, 14)
        self.display_text_formula('sp2', text1, text2, plus, 21)
        self.display_text_formula('sp3', text1, text2, plus, 28)
        if __name__ == '__main__':
            self.display_object.refresh()

    def display_text_formula(self, compare_text, text1, text2, plus, times):
        if self.name == compare_text:
            self.display_object.display_text_with_y(plus + times, text1)
            self.display_object.display_text_with_y(plus + 1 +  times, text2)

    def get_player(self):
        return self.player

    def get_name(self):
        return self.name

    def draw(self, deck, number_of_cards):
        self.cards.extend(deck.draw(number_of_cards))

    def is_blackjack(self):
        if len(self.cards) != 2:
            return False
        scores = [c.get_score() for c in self.cards]
        if sorted(scores) == [10, 11]:
            self.display_text('Black', 'jack', 2)
            return True
        return False

    def get_score(self):
        """ return sum of cards' score but return -999 if busted"""
        sum_score = sum([c.get_score() for c in self.cards])
        for c in self.cards:
            if c.get_value() == 'A' and sum_score > 21:
                sum_score -= 10
        self.display_text(str(sum_score), '', 4)
        return sum_score if sum_score <= 21 else -999

    def get_card_value(self, card_idx):
        return self.cards[card_idx].get_value()

    def is_busted(self):
        if self.get_score() < 0:
            self.display_text('Busted', '', 5)
        return self.get_score() < 0

    def get_card(self, index):
        return self.cards[index]

    def add_card(self, card):
        self.cards.append(card)

    def display_and_replace(self, y):
        self.card_count = 2
        self.already_displayed.append(self.cards[0])
        self.display_object.display_card_skeleton(y, 14, ' ')
        self.display_object.clear_card_symbol(y, 14, self.cards[1])

    def arrow(self, y):
        for x in range(6):
            self.display_object.display_text(y, x, '-')
        self.display_object.display_text(y, 6, '>')

    def display(self):
        if self.name == 'dealer':
            self.display_formula(0)
        elif self.name == 'player1':
            self.display_formula(1)
        elif self.name == 'sp1':
            self.display_formula(2)
        elif self.name == 'sp2':
            self.display_formula(3)
        elif self.name == 'sp3':
            self.display_formula(4)

    def check_in_list(self, list, element):
        for e in list:
            if e == element:
                return True
        return False


    def display_formula(self, a):
        for c in self.cards:
            if not self.check_in_list(self.already_displayed, c):
                self.display_object.display_card(a, self.card_count, c)
                self.card_count += 1
        for b in self.cards:
            self.already_displayed.append(b)
        return

    def clear_arrow(self):
        y_list = [3, 10, 17, 24, 32]
        for y in y_list:
            for x in range(7):
                self.display_object.display_text(y, x, ' ')

    def show_player(self):
        self.display_text(self.name, '', 0)

    def display_one_card(self):
        self.display_object.display_card(0, 1, self.cards[0])
        self.card_count = 2
        self.already_displayed.append(self.cards[0])
        self.display_object.display_card_skeleton(0, 14)

    def play(self, deck, game):
        self.player.show_all_players(game)
        if self.name == 'dealer':
            self.arrow(3)
        elif self.name == 'sp1':
            self.arrow(17)
        elif self.name == 'sp2':
            self.arrow(24)
        elif self.name == 'sp3':
            self.arrow(31)
        elif self.name == 'player1':
            self.arrow(10)
        while not (self.is_busted()) and not (self.is_blackjack()):
            self.display()
            self.display_object.display_text_times_seven(5, 'want to draw?')
            self.get_score()
            b = self.display_object.getstr(35, 14)
            draw_or_not = b.decode('utf-8')
            self.display_object.display_text(35, 14, ' ')
            if draw_or_not == 'y':
                self.draw(deck, 1)
            if draw_or_not == 'd':
                self.draw(deck, 1)
                break
            if draw_or_not == 's' and self.name != 'dealer':
                self.split()
            if draw_or_not == 'n':
                break
        self.get_score()
        self.display()
        self.clear_arrow()
        self.is_blackjack()

    def make_card(self, card):
        self.cards = [card]

    def splittable(self):
        return (len(self.cards) == 2) and (self.get_card_value(0) == self.get_card_value(1))

    def split(self):
        if not self.splittable():
            return
        first_card, second_card = self.cards
        new_hand = Player('sp' + str(self.player.counter)).create_hand(self.display_object)
        self.player.hands.append(new_hand)
        self.player.counter += 1
        if self.name == 'dealer':
            self.display_and_replace(0)
        elif self.name == 'player1':
            self.display_and_replace(7 * 1)
        elif self.name == 'sp1':
            self.display_and_replace(7 * 2)
        elif self.name == 'sp2':
            self.display_and_replace(7 * 3)
        elif self.name == 'sp3':
            self.display_and_replace(7 * 4)

        self.cards = [first_card]
        self.already_displayed.remove(second_card)
        new_hand.add_card(second_card)
        self.player.add_hand_to_play_queue(new_hand)
        new_hand.display()
        new_hand.show_player()

    def decide(self, other_hand):
        """return name of winner or tie if scores are equal"""
        # check blackjack cases
        if (self.is_blackjack() is True) and (other_hand.is_blackjack() is True):
            return 'Tie'
        if (self.is_blackjack() is True) and (other_hand.is_blackjack() is False):
            return f'{self.player.get_name()} won'
        if (self.is_blackjack() is False) and (other_hand.is_blackjack() is True):
            return f'{other_hand.player.get_name()} won'
        # check score cases
        if self.get_score() > other_hand.get_score():
            return f'{self.player.get_name()} won'
        elif self.get_score() < other_hand.get_score():
            return f'{other_hand.player.get_name()} won'
        else:
            return 'Tie'

    def __eq__(self, other):
        return (self.name == other.name) and (self.player == other.player) and (self.display_object == other.display_object)


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.hands = []
        self.queue = None
        self.counter = 1
        self.a_hand = None

    def get_name(self):
        return self.name

    def get_value(self, index, card):
        self.hands[index].get_value(card)

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
        return (self.name == other.get_name())


class Game:
    def __init__(self, stdscr):
        self.display_object = Display(stdscr)
        self.deck = Deck()
        self.deck.shuffle()
        self.players = []

    def get_deck(self):
        return self.deck

    def get_display(self):
        return self.display_object

    def create_player(self, player_name):
        a_player = Player(player_name)
        self.players.append(a_player)
        return a_player

    def get_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def initialize_player(self, player_name):
        a_player = self.create_player(player_name)
        a_player_hand = a_player.create_hand(self.display_object)
        a_player_hand.draw(self.deck, 2)
        return a_player, a_player_hand

    def play(self):
        # initialize both players
        player1, player1_hand = self.initialize_player('player1')
        dealer, dealer_hand = self.initialize_player('dealer')
        dealer_hand.display_one_card()
        # play both players
        for player in self.players:
            player.play(self.deck, self)
        # decide result by comparing dealer hand with each player's hand
        for self.number, hand in enumerate(player1.get_all_hands()):
            self.display_object.display_decide(self.number, f'Result for {hand.get_name()}')
            self.decide(dealer_hand, hand)

    def decide(self, h1, h2):
        self.display_object.display_decide(self.number, f'{h1.decide(h2)}', 1)


def main(stdscr):
    a = Game(stdscr)
    a.play()
    sleep(3)

if __name__ == '__main__':
    curses.wrapper(main)
    curses.echo()