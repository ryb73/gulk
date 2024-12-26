from dataclasses import dataclass
from typing import List, Optional
from .player import Player
from .deck import Deck
from .card import Card, Suit


@dataclass
class PlayedCard:
    card: Card
    player: Player


class TrickTakingGame:
    def __init__(self, player_names: List[str]):
        if len(player_names) < 2:
            raise ValueError("Need at least 2 players")

        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.current_trick: List[PlayedCard] = []
        self.trump_suit: Optional[Suit] = None

    def setup_round(self, cards_per_player: int):
        """Setup a new round of the game."""
        self.deck.build()
        self.current_trick = []
        self.current_trick_players = []

        # Validate cards per player
        max_cards = len(self.deck.cards) // len(self.players)
        if cards_per_player > max_cards:
            raise ValueError(f"Cannot deal {cards_per_player} cards per player. Maximum is {max_cards}")
        if cards_per_player < 1:
            raise ValueError("Must deal at least 1 card per player")

        # Deal specified number of cards to all players
        for player in self.players:
            player.add_cards(self.deck.take_cards(cards_per_player))

    def can_play_card(self, player: Player, card: Card) -> bool:
        """
        Check if playing a card would be valid.
        Returns True if the play would be valid, False otherwise.
        """
        if len(self.current_trick) == len(self.players):
            return False  # Trick is already full

        # Add basic trick-following rules here
        if len(self.current_trick) > 0:
            led_suit = self.current_trick[0].card.suit
            if card.suit != led_suit and any(c.suit == led_suit for c in player.hand):
                return False  # Must follow suit if possible

        return True

    def play_card(self, player: Player, card: Card) -> bool:
        """
        Handle a player playing a card.
        Returns True if the play was successful, False otherwise.
        """
        if not self.can_play_card(player, card):
            return False

        player.remove_card(card)
        self.current_trick.append(PlayedCard(card, player))
        return True

    def evaluate_trick(self) -> Optional[Player]:
        """
        Evaluate the current trick and return the winning player.
        Returns None if the trick is not complete.
        """
        if len(self.current_trick) != len(self.players):
            return None

        led_suit = self.current_trick[0].card.suit
        winning_played_card = self.current_trick[0]
        winner_index = 0

        for i, played in enumerate(self.current_trick[1:], 1):
            card = played.card
            # If trump suit is played, it wins over non-trump
            if self.trump_suit:
                if (
                    card.suit == self.trump_suit
                    and winning_played_card.card.suit != self.trump_suit
                ):
                    winning_played_card = played
                    winner_index = i
                elif (
                    card.suit == winning_played_card.card.suit
                    and card.rank.value > winning_played_card.card.rank.value
                ):
                    winning_played_card = played
                    winner_index = i
            # No trump suit - follow basic trick-taking rules
            elif (
                card.suit == led_suit
                and card.rank.value > winning_played_card.card.rank.value
            ):
                winning_played_card = played
                winner_index = i

        winning_player = self.current_trick[winner_index].player
        winning_player.win_trick([played.card for played in self.current_trick])
        self.current_trick = []
        return winning_player
