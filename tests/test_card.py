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
    assert str(card) == "KING of DIAMONDS"
