from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
from .player import Player
from .game_round import GameRound


@dataclass
class RoundScore:
    points: Dict[Player, int]


class RoundScorer(ABC):
    @abstractmethod
    def score_round(self, round: GameRound) -> RoundScore:
        """Calculate scores for the round"""
        pass


class BiddingScorer(RoundScorer):
    def __init__(self):
        self._bids = None

    @staticmethod
    def create() -> "BiddingScorer":
        """Factory method that creates an empty scorer"""
        return BiddingScorer()

    def set_bids(self, bids: Dict[Player, int], num_tricks: int) -> bool:
        """
        Set the bids for this round.
        Returns True if bids are valid, False otherwise.
        """
        if sum(bids.values()) == num_tricks:  # Invalid if bids sum to tricks
            return False
        self._bids = bids
        return True

    def score_round(self, round: GameRound) -> RoundScore:
        if self._bids is None:
            raise ValueError("Bids must be set before scoring")

        scores = {}
        for player in round.players:
            tricks_taken = len(round.tricks_won[player])
            if tricks_taken == self._bids[player]:
                scores[player] = 10 + self._bids[player]
            else:
                scores[player] = 0
        return RoundScore(scores)


class AllOrNothingScorer(RoundScorer):
    def score_round(self, round: GameRound) -> RoundScore:
        scores = {}
        total_tricks = sum(len(tricks) for tricks in round.tricks_won.values())

        for player in round.players:
            tricks_taken = len(round.tricks_won[player])
            if tricks_taken == total_tricks:
                scores[player] = 10
                # Penalize others
                for other in round.players:
                    if other != player:
                        scores[other] = -10

                # All players have now been scored
                break
            else:
                scores[player] = -2 * tricks_taken
        return RoundScore(scores)


class FixedBidScorer(RoundScorer):
    def __init__(self, target_tricks: int = 3, points: int = 20):
        self.target_tricks = target_tricks
        self.points = points

    def score_round(self, round: GameRound) -> RoundScore:
        return RoundScore(
            {
                player: (
                    self.points
                    if len(round.tricks_won[player]) == self.target_tricks
                    else 0
                )
                for player in round.players
            }
        )
