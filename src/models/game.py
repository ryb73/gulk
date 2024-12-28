from dataclasses import dataclass
from typing import List, Optional, Union
from .player import Player
from .deck import Deck
from .card import Card, Suit


@dataclass
class PlayedCard:
    card: Card
    player: Player


class TrickTakingGame:
    def __init__(self, player_names: List[str], deck: Optional[Deck] = None):
        if len(player_names) < 2:
            raise ValueError("Need at least 2 players")

        self.players = [Player(name) for name in player_names]
        self.deck = deck if deck is not None else Deck()
        self.current_trick: List[PlayedCard] = []
        self.trump_suit: Optional[Suit] = None

    def setup_round(self, cards_per_player: int, trump: bool = True):
        """Setup a new round of the game."""
        self.deck.build()
        self.current_trick = []
        self.trump_suit = None

        # Validate cards per player
        total_needed = cards_per_player * len(self.players)
        if trump:
            total_needed += 1  # Account for trump card

        if total_needed > len(self.deck.cards):
            raise ValueError(f"Not enough cards for {cards_per_player} per player")
        if cards_per_player < 1:
            raise ValueError("Must deal at least 1 card per player")

        # Deal specified number of cards to all players
        for player in self.players:
            player.add_cards(self.deck.take_cards(cards_per_player))

        # Draw trump card if enabled
        if trump:
            trump_card = self.deck.take_cards(1)[0]
            self.trump_suit = trump_card.suit

    def can_play_card(self, player: Player, card: Card) -> Union[str, bool]:
        """
        Check if playing a card would be valid.
        Returns True if the play is valid, or a string explaining why it's invalid.
        """
        if len(self.current_trick) == len(self.players):
            return "Trick is already complete"

        # First card of trick can be anything
        if len(self.current_trick) == 0:
            return True

        # Must follow suit if possible
        led_suit = self.current_trick[0].card.suit
        has_led_suit = any(c.suit == led_suit for c in player.hand)

        if has_led_suit and card.suit != led_suit:
            matching_cards = [c for c in player.hand if c.suit == led_suit]
            return f"Must follow suit with one of: {', '.join(str(c) for c in matching_cards)}"

        return True

    def play_card(self, player: Player, card: Card) -> None:
        """
        Handle a player playing a card.
        Raises ValueError with explanation if the play is invalid.
        """
        result = self.can_play_card(player, card)
        if result is not True:
            raise ValueError(result)

        player.remove_card(card)
        self.current_trick.append(PlayedCard(card, player))

    def evaluate_trick(self) -> Player:
        """
        Evaluate the current trick and return the winning player.
        Raises ValueError if the trick is not complete.
        """
        if len(self.current_trick) != len(self.players):
            raise ValueError(
                f"Cannot evaluate incomplete trick. Expected {len(self.players)} cards, got {len(self.current_trick)}"
            )

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
