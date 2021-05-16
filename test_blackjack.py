from Blackjack import Card, Deck, Hand, Player, Game
from collections import deque

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
    hand_object.add_card(Card('A', 'S'))
    assert hand_object.get_card(0) == Card('A', 'S')

def test_make_card():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.make_card(Card('A', 'S'))
    assert hand_object.get_card(0) == Card('A','S')

def test_get_card_value():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.add_card(Card('A', 'S'))
    assert hand_object.get_card_value(0) == 'A'

def test_splittable():
    hand_object = Hand('Player1', 'Player_object', 'None')
    hand_object.cards = [Card('A', 'S'), Card('A', 'C')]
    assert hand_object.splittable() == True
    hand_object.cards = [Card('A', 'S'), Card('2', 'C')]
    assert hand_object.splittable() == False
    hand_object.cards = [Card('A', 'S'), Card('A', 'C'), Card('A', 'D')]
    assert hand_object.splittable() == False

def test_decide():
    player_object = Player('Player1', Deck(), 'Game_object')
    dealer_object = Player('Dealer', Deck(), 'Game_object')
    hand_object = Hand('Player1', player_object, 'None')
    other_hand_object = Hand('Dealer', dealer_object, 'None')
    hand_object.cards = [Card('A','S'), Card('J','S')]
    other_hand_object.cards = [Card('A','S'), Card('10','S')]
    assert hand_object.decide(other_hand_object) == 'Tie'
    hand_object.cards = [Card('A','S'), Card('J','S')]
    other_hand_object.cards = [Card('2','S'), Card('10','S')]
    assert hand_object.decide(other_hand_object) == f'{player_object.get_name()} won'
    hand_object.cards = [Card('2','S'), Card('10','S')]
    other_hand_object.cards = [Card('A','S'), Card('J','S')]
    assert hand_object.decide(other_hand_object) == f'{dealer_object.get_name()} won'
    hand_object.cards = [Card('3','S'), Card('J','S')]
    other_hand_object.cards = [Card('2','S'), Card('10','S')]
    assert hand_object.decide(other_hand_object) == f'{player_object.get_name()} won'
    hand_object.cards = [Card('2','S'), Card('10','S')]
    other_hand_object.cards = [Card('3','S'), Card('J','S')]
    assert hand_object.decide(other_hand_object) == f'{dealer_object.get_name()} won'
    hand_object.cards = [Card('5','D'), Card('J','S')]
    other_hand_object.cards = [Card('5','S'), Card('10','S')]
    assert hand_object.decide(other_hand_object) == 'Tie'

def test_Hand_equal():
    hand_object = Hand('Player1', 'Player_object', 'None')
    comparing_object = Hand('Player', 'Player_object', 'None')
    assert not hand_object == comparing_object
    hand_object = Hand('Player1', 'Player_object', 'None')
    comparing_object = Hand('Player1', 'Player_objec', 'None')
    assert not hand_object == comparing_object
    hand_object = Hand('Player1', 'Player_object', 'None')
    comparing_object = Hand('Player1', 'Player_object', 'Non')
    assert not hand_object == comparing_object
    hand_object = Hand('Player1', 'Player_object', 'None')
    comparing_object = Hand('Player1', 'Player_object', 'None')
    assert hand_object == comparing_object

def test_get_name():
    player_object  = Player('Player1', "Deck()", 'game_object')
    assert player_object.get_name() == 'Player1' 

def test_create_hand():
    player_object = Player('Player1', Deck(), 'Game_object')
    assert player_object.create_hand('Player1', 'display_object') == Hand('Player1', player_object, 'display_object')

def test_get_hand():
    player_object = Player('Player1', Deck(), 'Game_object')
    player_object.create_hand('Player1', 'display_object')
    assert player_object.get_hand() == Hand('Player1', player_object, 'display_object')

def test_get_all_hands():
    player_object = Player('Player1', Deck(), 'Game_object')
    player_object.create_hand('Player1', 'display_object')
    player_object.create_hand('Dealer', 'display_object')
    assert player_object.get_all_hands()[0] == Hand('Player1', player_object, 'display_object')

def test_add_hand_to_play_queue():
    player_object = Player('Player1', Deck(), 'Game_object')
    player_object.create_hand('Player1', 'display_object')
    player_object.queue = deque(player_object.hands)
    hand = Hand('Dealer', player_object, 'display_object')
    player_object.add_hand_to_play_queue(hand)
    assert len(player_object.queue) == 2

def test_equal_Player():
    player_object = Player('Player1', 'Deck_object', 'game_object')
    comparing_object = Player('Player', 'Deck_object', 'game_object')
    assert not player_object == comparing_object
    player_object = Player('Player1', 'Deck_object', 'game_object')
    comparing_object = Player('Player1', 'Deck_objec', 'game_object')
    assert not player_object == comparing_object
    player_object = Player('Player1', 'Deck_object', 'game_object')
    comparing_object = Player('Player1', 'Deck_object', 'game_objec')
    assert not player_object == comparing_object
    player_object = Player('Player1', 'Deck_object', 'game_object')
    comparing_object = Player('Player1', 'Deck_object', 'game_object')
    assert player_object == comparing_object

def test_get_deck():
    game_object = Game('stdscr')
    assert game_object.Display == game_object.get_display()

def test_create_player():
    game_object = Game('stdscr')
    player_object = Player('Player1', game_object.get_deck(), game_object)
    assert game_object.create_player('Player1') == player_object

def test_get_player():
    game_object = Game('stdscr')
    player_object = Player('Player1', game_object.get_deck(), game_object)
    game_object.create_player('Player1')
    assert game_object.get_player('Player1') == player_object

def test_initualize_player():
    game_object = Game('stdscr')
    player_object = Player('Player1', game_object.get_deck(), game_object)
    hand_object = Hand('Player1', player_object, game_object.get_display())
    p, h = game_object.initialize_player('Player1')
    assert p == player_object
    assert h == hand_object