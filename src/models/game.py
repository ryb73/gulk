from typing import List, Optional
from .player import Player
from .deck import Deck
from .card import Card, Suit


class TrickTakingGame:
    def __init__(self, player_names: List[str]):
        if len(player_names) < 2:
            raise ValueError("Need at least 2 players")

        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.current_trick: List[Card] = []
        self.trump_suit: Optional[Suit] = None

    def setup_round(self):
        """Setup a new round of the game."""
        self.deck.build()
        self.current_trick = []

        # Deal cards evenly to all players
        cards_per_player = len(self.deck.cards) // len(self.players)
        for player in self.players:
            player.add_cards(self.deck.take_cards(cards_per_player))

    def can_play_card(self, player: Player, card: Card) -> bool:
        """
        Handle a player playing a card.
        Returns True if the play is valid, False otherwise.
        """
        if len(self.current_trick) == len(self.players):
            return False  # Trick is already full

        # Add basic trick-following rules here
        if len(self.current_trick) > 0:
            led_suit = self.current_trick[0].suit
            if card.suit != led_suit and any(c.suit == led_suit for c in player.hand):
                return False  # Must follow suit if possible

        player.remove_card(card)
        self.current_trick.append(card)
        return True

    def evaluate_trick(self) -> Optional[Player]:
        """
        Evaluate the current trick and return the winning player.
        Returns None if the trick is not complete.
        """
        if len(self.current_trick) != len(self.players):
            return None

        led_suit = self.current_trick[0].suit
        winning_card = self.current_trick[0]
        winner_index = 0

        for i, card in enumerate(self.current_trick[1:], 1):
            # If trump suit is played, it wins over non-trump
            if self.trump_suit:
                if (
                    card.suit == self.trump_suit
                    and winning_card.suit != self.trump_suit
                ):
                    winning_card = card
                    winner_index = i
                elif (
                    card.suit == winning_card.suit
                    and card.rank.value > winning_card.rank.value
                ):
                    winning_card = card
                    winner_index = i
            # No trump suit - follow basic trick-taking rules
            elif card.suit == led_suit and card.rank.value > winning_card.rank.value:
                winning_card = card
                winner_index = i

        winning_player = self.players[winner_index]
        winning_player.win_trick(self.current_trick)
        self.current_trick = []
        return winning_player
