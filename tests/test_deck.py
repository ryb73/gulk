import pytest
from src.models.deck import Deck


def test_deck_creation():
    deck = Deck()
    assert len(deck.cards) == 52


def test_dealing():
    deck = Deck()
    initial_size = len(deck.cards)

    dealt = deck.take_cards(5)
    assert len(dealt) == 5
    assert len(deck.cards) == initial_size - 5


def test_dealing_too_many():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.take_cards(53)
