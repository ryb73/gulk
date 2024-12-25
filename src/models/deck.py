from typing import List
import random
from .card import Card, Suit, Rank

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.build()

    def build(self):
        """Creates a standard 52-card deck."""
        self.cards = [
            Card(suit, rank)
            for suit in Suit
            for rank in Rank
        ]

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int = 1) -> List[Card]:
        """Deals the specified number of cards from the top of the deck."""
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck")
        dealt_cards = self.cards[-num_cards:]
        self.cards = self.cards[:-num_cards]
        return dealt_cards
