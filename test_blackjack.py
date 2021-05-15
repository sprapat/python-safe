from Blackjack import Card, Deck


def test_card():
    card_object = Card('K','S')
    assert card_object.get_value() == 'K'
    assert card_object.get_suit() == 'S'
    assert card_object.get_score() == 10
    card_object = Card('Q','S')
    assert card_object.get_value() == 'Q'
    assert card_object.get_suit() == 'S'
    assert card_object.get_score() == 10
    card_object = Card('J','S')
    assert card_object.get_value() == 'J'
    assert card_object.get_suit() == 'S'
    assert card_object.get_score() == 10
    card_object = Card('A','S')
    assert card_object.get_value() == 'A'
    assert card_object.get_suit() == 'S'
    assert card_object.get_score() == 11
    card_object = Card('5','S')
    assert card_object.get_value() == '5'
    assert card_object.get_suit() == 'S'
    assert card_object.get_score() == 5
# display_object = Display(curses.initscr())
# def test_deck():
#     deck_display = Deck(display_object)
#     assert deck_display.draw(1).get_value == 'A'


