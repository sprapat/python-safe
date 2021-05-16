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

def test_compare_card():
    assert Card('K','S') == Card('K','S')
    assert Card('K','S') != Card('Q','S')
    assert Card('K','S') != Card('K','C')

def test_draw():
    deck_object = Deck()
    for i in deck_object.draw(1):
        print(i.get_value,i.get_score)
    assert deck_object.draw(1)[0] == Card('A','C')
   
    
def test_shuffle():
    deck_object = Deck()
    value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
    suit = ['C', 'H', 'S', 'D']
    cards = [Card(v, s) for v in value for s in suit]

    assert all([a==b for a,b in zip(deck_object.get_deck(), cards)])
    deck_object.shuffle()
    assert not all([a==b for a,b in zip(deck_object.get_deck(), cards)])

    # assert all(deck_object.get_deck() == cards)
    # assert deck_object.shuffle() != cards




