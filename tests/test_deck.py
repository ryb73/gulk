import pytest
from src.models.deck import Deck

def test_deck_creation():
    deck = Deck.standard_deck()
    assert len(deck.cards) == 52

def test_dealing():
    deck = Deck.standard_deck()
    initial_size = len(deck.cards)

    dealt = deck.take_cards(5)
    assert len(dealt) == 5
    assert len(deck.cards) == initial_size - 5

def test_dealing_too_many():
    deck = Deck.standard_deck()
    with pytest.raises(ValueError):
        deck.take_cards(53)

def test_custom_deck():
    from src.models.card import Card, Suit, Rank
    cards = [
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.SPADES, Rank.KING),
    ]
    deck = Deck(cards)
    assert len(deck.cards) == 2
    assert deck.cards[0].suit == Suit.HEARTS
    assert deck.cards[1].suit == Suit.SPADES
