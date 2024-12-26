import pytest
from src.models.card import Card, Suit, Rank


def test_card_creation():
    card = Card(Suit.HEARTS, Rank.ACE)
    assert card.suit == Suit.HEARTS
    assert card.rank == Rank.ACE


def test_card_comparison():
    lower = Card(Suit.HEARTS, Rank.TEN)
    higher = Card(Suit.SPADES, Rank.ACE)
    assert lower < higher
    assert higher > lower


def test_card_str():
    card = Card(Suit.DIAMONDS, Rank.KING)
    assert str(card) == "K♦"


def test_card_str_numeric():
    card2 = Card(Suit.HEARTS, Rank.TWO)
    card10 = Card(Suit.CLUBS, Rank.TEN)
    assert str(card2) == "2♥"
    assert str(card10) == "10♣"


def test_card_str_face_cards():
    jack = Card(Suit.SPADES, Rank.JACK)
    queen = Card(Suit.HEARTS, Rank.QUEEN)
    king = Card(Suit.CLUBS, Rank.KING)
    ace = Card(Suit.DIAMONDS, Rank.ACE)
    assert str(jack) == "J♠"
    assert str(queen) == "Q♥"
    assert str(king) == "K♣"
    assert str(ace) == "A♦"


def test_card_str_all_suits():
    rank = Rank.SEVEN
    hearts = Card(Suit.HEARTS, rank)
    diamonds = Card(Suit.DIAMONDS, rank)
    clubs = Card(Suit.CLUBS, rank)
    spades = Card(Suit.SPADES, rank)
    assert str(hearts) == "7♥"
    assert str(diamonds) == "7♦"
    assert str(clubs) == "7♣"
    assert str(spades) == "7♠"
