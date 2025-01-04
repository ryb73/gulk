import pytest
from src.models.scoring import (
    BiddingScorer,
    AllOrNothingScorer,
    FixedBidScorer,
    RoundScore,
)
from src.models.game_round import GameRound
from src.models.card import Card, Suit
from src.models.player import Player


def create_test_round(player_names: list[str]) -> GameRound:
    round = GameRound(player_names)
    round.setup_round(cards_per_player=3, trump=False)
    return round


def simulate_tricks(round: GameRound, trick_winners: list[Player]) -> None:
    """Simulate tricks being won by specified players"""
    for winner in trick_winners:
        round.tricks_won[winner].append([])  # Empty list represents a trick


class TestBiddingScorer:
    def test_correct_bids(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate Alice winning 2 tricks, Bob winning 1
        simulate_tricks(round, [alice, alice, bob])

        # Test when both players meet their bids
        scorer = BiddingScorer.create({alice: 2, bob: 1}, num_tricks=3)
        assert scorer is not None

        score = scorer.score_round(round)
        assert score.points[alice] == 12  # 10 + bid of 2
        assert score.points[bob] == 11  # 10 + bid of 1

    def test_incorrect_bids(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate Bob winning all tricks
        simulate_tricks(round, [bob, bob, bob])

        scorer = BiddingScorer.create({alice: 2, bob: 0}, num_tricks=3)
        assert scorer is not None

        score = scorer.score_round(round)
        assert score.points[alice] == 0  # Failed bid
        assert score.points[bob] == 0  # Failed bid

    def test_invalid_bids(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Bids sum to number of tricks (invalid)
        scorer = BiddingScorer.create({alice: 2, bob: 1}, num_tricks=3)
        assert scorer is not None

        # Bids sum to tricks (invalid)
        invalid_scorer = BiddingScorer.create({alice: 1, bob: 2}, num_tricks=3)
        assert invalid_scorer is None


class TestAllOrNothingScorer:
    def test_all_tricks_winner(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate Alice winning all tricks
        simulate_tricks(round, [alice, alice, alice])

        scorer = AllOrNothingScorer()
        score = scorer.score_round(round)

        assert score.points[alice] == 10  # Won all tricks
        assert score.points[bob] == -10  # Lost all tricks

    def test_split_tricks(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate split tricks
        simulate_tricks(round, [alice, bob, alice])

        scorer = AllOrNothingScorer()
        score = scorer.score_round(round)

        assert score.points[alice] == -4  # -2 per trick taken
        assert score.points[bob] == -2  # -2 per trick taken


class TestFixedBidScorer:
    def test_exact_target(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate Alice winning exactly 3 tricks
        simulate_tricks(round, [alice, alice, alice])

        scorer = FixedBidScorer(target_tricks=3, points=20)
        score = scorer.score_round(round)

        assert score.points[alice] == 20  # Met target
        assert score.points[bob] == 0  # Didn't meet target

    def test_custom_target(self):
        round = create_test_round(["Alice", "Bob"])
        alice, bob = round.players

        # Simulate split tricks
        simulate_tricks(round, [alice, bob, alice])

        scorer = FixedBidScorer(target_tricks=2, points=15)
        score = scorer.score_round(round)

        assert score.points[alice] == 15  # Met target of 2
        assert score.points[bob] == 0  # Didn't meet target
