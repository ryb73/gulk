from dataclasses import dataclass
from typing import List, Optional, Dict
from .player import Player
from .deck import Deck
from .card import Card, Suit


@dataclass
class PlayedCard:
    card: Card
    player: Player


class GameRound:
    def __init__(self, player_names: List[str]):
        if len(player_names) < 2:
            raise ValueError("Need at least 2 players")

        self.players = [Player(name) for name in player_names]
        self.current_trick: List[PlayedCard] = []
        self.trump_suit: Optional[Suit] = None
        self.tricks_won: Dict[Player, List[List[Card]]] = {
            player: [] for player in self.players
        }
        self.hands: Dict[Player, List[Card]] = {player: [] for player in self.players}

    def get_hand(self, player: Player) -> List[Card]:
        """Get a player's current hand."""
        return self.hands[player]

    def add_cards_to_hand(self, player: Player, cards: List[Card]):
        """Add cards to a player's hand."""
        self.hands[player].extend(cards)

    def remove_card_from_hand(self, player: Player, card: Card) -> Card:
        """Remove a card from a player's hand."""
        if card not in self.hands[player]:
            raise ValueError("Card not in hand")
        self.hands[player].remove(card)
        return card

    def setup_round(
        self, cards_per_player: int, trump: bool = True, deck: Optional[Deck] = None
    ):
        """Setup a new round of the game."""
        self.current_trick = []
        self.trump_suit = None
        self.tricks_won = {player: [] for player in self.players}
        self.hands = {player: [] for player in self.players}

        # Initialize deck
        self.deck = deck if deck is not None else Deck.standard_deck()

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
            self.add_cards_to_hand(player, self.deck.take_cards(cards_per_player))

        # Draw trump card if enabled
        if trump:
            trump_card = self.deck.take_cards(1)[0]
            self.trump_suit = trump_card.suit

    def check_play_validity(self, player: Player, card: Card) -> Optional[str]:
        """
        Check if playing a card would be valid.
        Returns None if the play is valid, or a string explaining why it's invalid.
        """
        if len(self.current_trick) == len(self.players):
            return "Trick is already complete"

        # First card of trick can be anything
        if len(self.current_trick) == 0:
            return None

        # Must follow suit if possible
        led_suit = self.current_trick[0].card.suit
        hand = self.hands[player]
        has_led_suit = any(c.suit == led_suit for c in hand)

        if has_led_suit and card.suit != led_suit:
            matching_cards = [c for c in hand if c.suit == led_suit]
            return f"Must follow suit with one of: {', '.join(str(c) for c in matching_cards)}"

        return None

    def play_card(self, player: Player, card: Card) -> None:
        """
        Handle a player playing a card.
        Raises ValueError with explanation if the play is invalid.
        """
        result = self.check_play_validity(player, card)
        if result is not None:
            raise ValueError(result)

        self.remove_card_from_hand(player, card)
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
        trick_cards = [played.card for played in self.current_trick]
        self.tricks_won[winning_player].append(trick_cards)
        self.current_trick = []
        return winning_player

    def is_over(self) -> bool:
        """Check if the game is over."""
        # Don't end during incomplete trick
        if self.current_trick and len(self.current_trick) < len(self.players):
            return False

        # End when all players are out of cards
        return all(len(self.hands[player]) == 0 for player in self.players)
