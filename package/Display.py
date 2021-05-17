import curses

class Display:
    SUIT_CHR = {'S': '\u2660', 'H': '\u2665', 'D': '\u2666', 'C': '\u2663'}

    def __init__(self, stdscr):
        self.stdscr = stdscr

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
        self.display_card_skeleton(y * 7, x * 7)
        self.display_card_symbol(y * 7, x * 7, card.get_value(), card.get_suit())
        self.refresh()