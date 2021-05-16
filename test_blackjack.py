from Blackjack import Card, Deck, Hand

# assert True == False
def test_get_value():
    card_object = Card('K','S')
    assert card_object.get_value() == 'K'
    card_object = Card('Q','S')
    assert card_object.get_value() == 'Q'
    card_object = Card('J','S')
    assert card_object.get_value() == 'J'
    card_object = Card('A','S')
    assert card_object.get_value() == 'A'
    card_object = Card('5','S')
    assert card_object.get_value() == '5'

def test_get_suit():
    card_object = Card('K','C')
    assert card_object.get_suit() == 'C'
    card_object = Card('K','H')
    assert card_object.get_suit() == 'H'
    card_object = Card('K','S')
    assert card_object.get_suit() == 'S'
    card_object = Card('K','D')
    assert card_object.get_suit() == 'D'
def test_get_score():
    card_object = Card('K','S')
    assert card_object.get_score() == 10
    card_object = Card('Q','S')
    assert card_object.get_score() == 10
    card_object = Card('J','S')
    assert card_object.get_score() == 10
    card_object = Card('A','S')
    assert card_object.get_score() == 11
    card_object = Card('5','S')
    assert card_object.get_score() == 5

def test_compare_card():
    assert Card('K','S') == Card('K','S')
    assert Card('K','S') != Card('Q','S')
    assert Card('K','S') != Card('K','C')

def test_draw():
    deck_object = Deck()
    # print(deck_object.draw(4))
    assert all([a==b for a,b in zip(deck_object.draw(4), [Card('A','C'), Card('A','H'), Card('A','S'), Card('A','D')])])
    
def test_shuffle():
    deck_object = Deck()
    value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
    suit = ['C', 'H', 'S', 'D']
    cards = [Card(v, s) for v in value for s in suit]

    assert all([a==b for a,b in zip(deck_object.get_deck(), cards)])
    deck_object.shuffle()
    assert not all([a==b for a,b in zip(deck_object.get_deck(), cards)])

def test_get_player():
    assert Hand('Player1', 'Player_object', 'None').get_player() == 'Player_object'

def test_get_name():
    assert Hand('Player1', 'Player_object', 'None').get_name() == 'Player1'

def test_add_card():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.add_card(Card('A','S'))
    assert hand_object.cards[0] == Card('A','S')

def test_Hand_draw():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.draw(Deck(), 1)
    assert hand_object.cards[0] == Card('A','C')


def test_get_score():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.cards = [Card('A','S'), Card('10','S')]
    assert hand_object.get_score() == 21
    hand_object.cards = [Card('A','S'), Card('10','S'), Card('A','C')]
    assert hand_object.get_score() == 12

def test_is_blackjack():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.cards = [Card('A','S'), Card('10','S')]
    assert hand_object.is_blackjack() == True
    hand_object.cards = [Card('A','S'), Card('J','S')]
    assert hand_object.is_blackjack() == True
    hand_object.cards = [Card('A','S'), Card('Q','S')]
    assert hand_object.is_blackjack() == True
    hand_object.cards = [Card('A','S'), Card('K','S')]
    assert hand_object.is_blackjack() == True
    hand_object.cards = [Card('A','S'), Card('10','S'), Card('A','C')]
    assert hand_object.is_blackjack() == False
    hand_object.cards = [Card('2','S'), Card('10','S')]
    assert hand_object.is_blackjack() == False
    hand_object.cards = [Card('A','S'), Card('2','S')]
    assert hand_object.is_blackjack() == False

def test_is_busted():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.cards = [Card('A','S'), Card('10','S')]
    assert hand_object.is_busted() == False
    hand_object.cards = [Card('A','S'), Card('J','S')]
    assert hand_object.is_busted() == False
    hand_object.cards = [Card('A','S'), Card('Q','S')]
    assert hand_object.is_busted() == False
    hand_object.cards = [Card('A','S'), Card('K','S')]
    assert hand_object.is_busted() == False
    hand_object.cards = [Card('A','S'), Card('10','S'), Card('A','C')]
    assert hand_object.is_busted() == False
    hand_object.cards = [Card('K','S'), Card('10','S'), Card('2','C')]
    assert hand_object.is_busted() == True

def test_get_card():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.add_card(Card('A','S'))
    assert hand_object.get_card(0) == Card('A','S')

def test_make_card():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.make_card(Card('A','S'))
    assert hand_object.get_card(0) == Card('A','S')



