from typing import List, Sequence
import random
from .card import Card, Suit, Rank


class Deck:
    STANDARD_DECK_SIZE = 52

    def __init__(self, cards: Sequence[Card]):
        """Initialize a deck with a specific sequence of cards."""
        self._cards = tuple(cards)

    @classmethod
    def standard_deck(cls) -> "Deck":
        """Creates a shuffled standard 52-card deck."""
        cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(cards)
        return cls(cards)

    @property
    def cards(self) -> tuple[Card, ...]:
        return self._cards

    def take_cards(self, num_cards: int = 1) -> List[Card]:
        """Deals the specified number of cards from the top of the deck."""
        if num_cards > len(self._cards):
            raise ValueError("Not enough cards left in the deck")
        new_cards = self._cards[:-num_cards]
        dealt_cards = list(self._cards[-num_cards:])
        self._cards = new_cards
        print(f"Dealt cards: {dealt_cards}")
        return dealt_cards
