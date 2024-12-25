from typing import List
from .card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.tricks_won: List[List[Card]] = []

    def receive_cards(self, cards: List[Card]):
        """Add cards to the player's hand."""
        self.hand.extend(cards)

    def play_card(self, card: Card) -> Card:
        """Play a card from the player's hand."""
        if card not in self.hand:
            raise ValueError("Card not in hand")
        self.hand.remove(card)
        return card

    def win_trick(self, trick: List[Card]):
        """Add a won trick to the player's collection."""
        self.tricks_won.append(trick)
