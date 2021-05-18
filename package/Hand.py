class Hand:
    def __init__(self, player, display, name = None):
        self.cards = []
        self.player = player
        if type(name) == str:
            self.name = name
        else:
            self.name = self.player.get_name()
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
        if self.name == 'dealer':
            self.arrow(3)
        elif self.name == 'player1':
            self.arrow(10)
        elif self.name == 'sp1':
            self.arrow(17)
        elif self.name == 'sp2':
            self.arrow(24)
        elif self.name == 'sp3':
            self.arrow(31)
        self.player.show_all_players(game)
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
        new_hand = Hand(self.player, self.display_object, 'sp' + str(self.player.get_counter()))
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
        first_card = self.cards[0]
        second_card = self.cards[1]
        self.cards = [first_card]
        self.already_displayed.remove(second_card)
        new_hand.add_card(second_card)
        self.player.add_hand_to_play_queue(new_hand)
        self.player.hands.append(new_hand)
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