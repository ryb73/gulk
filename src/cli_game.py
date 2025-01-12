from dataclasses import dataclass
from typing import List, Type
from src.models.game_round import GameRound
from src.models.player import Player
from src.models.scoring import (
    RoundScorer,
    BiddingScorer,
    AllOrNothingScorer,
    FixedBidScorer,
    RoundScore,
)
from src.cli_helpers import get_bids, play_round_loop

@dataclass
class RoundConfig:
    cards_per_player: int
    use_trump: bool
    scorer_type: Type[RoundScorer]
    scorer_params: dict

class GameController:
    def __init__(self, player_names: List[str]):
        self.players = [Player(name) for name in player_names]
        self.total_scores = {player: 0 for player in self.players}
        self.round_configs = self._setup_round_configs()

    def _setup_round_configs(self) -> List[RoundConfig]:
        """Define the 20 rounds of the game"""
        configs = []

        # Rounds 1-5: Bidding rounds with decreasing cards (10 to 6)
        for cards in range(10, 5, -1):
            configs.append(RoundConfig(
                cards_per_player=cards,
                use_trump=True,
                scorer_type=BiddingScorer,
                scorer_params={}
            ))

        # Rounds 6-10: All or Nothing rounds with increasing cards (6 to 10)
        for cards in range(6, 11):
            configs.append(RoundConfig(
                cards_per_player=cards,
                use_trump=True,
                scorer_type=AllOrNothingScorer,
                scorer_params={}
            ))

        # Rounds 11-15: Fixed Bid rounds with varying targets
        for cards, target in zip(range(8, 13), range(2, 7)):
            configs.append(RoundConfig(
                cards_per_player=cards,
                use_trump=False,
                scorer_type=FixedBidScorer,
                scorer_params={'target_tricks': target, 'points': 20}
            ))

        # Rounds 16-20: Bidding rounds without trump
        for cards in range(10, 5, -1):
            configs.append(RoundConfig(
                cards_per_player=cards,
                use_trump=False,
                scorer_type=BiddingScorer,
                scorer_params={}
            ))

        return configs

    def play_game(self):
        print("Starting new game with players:", ", ".join(p.name for p in self.players))

        for round_num, config in enumerate(self.round_configs, 1):
            print(f"\n=== Round {round_num} of {len(self.round_configs)} ===")
            print(f"Cards per player: {config.cards_per_player}")
            print(f"Trump suits: {'Enabled' if config.use_trump else 'Disabled'}")
            print(f"Scoring: {config.scorer_type.__name__}")

            round = GameRound(self.players)
            round.setup_round(config.cards_per_player, trump=config.use_trump)

            # Create scorer based on config
            scorer = config.scorer_type(**config.scorer_params)

            self._play_round(round, scorer)
            round_score = scorer.score_round(round)

            # Update total scores
            for player, points in round_score.points.items():
                self.total_scores[player] += points

            self._display_scores(round_num, round_score)

        self._display_final_scores()

    def _play_round(self, round: GameRound, scorer: RoundScorer):
        if isinstance(scorer, BiddingScorer):
            num_tricks = len(round.get_hand(round.players[0]))
            bids = get_bids(round.players, num_tricks)
            if not scorer.set_bids(bids, num_tricks):
                raise ValueError("Invalid bids")

        play_round_loop(round)

        print("\nRound Over!")
        for player in round.players:
            print(f"{player.name}: {len(round.tricks_won[player])} tricks")

    def _display_scores(self, round_num: int, round_score: RoundScore):
        print(f"\nScores after round {round_num}:")
        print("Round scores:")
        for player, points in round_score.points.items():
            print(f"{player.name}: {points}")
        print("\nTotal scores:")
        for player, total in self.total_scores.items():
            print(f"{player.name}: {total}")

    def _display_final_scores(self):
        print("\n=== Final Scores ===")
        # Sort players by score
        sorted_players = sorted(
            self.players,
            key=lambda p: self.total_scores[p],
            reverse=True
        )
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.name}: {self.total_scores[player]}")

def main():
    print("Welcome to the Card Game!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            print("Please enter a number between 2 and 4.")
        except ValueError:
            print("Please enter a valid number.")

    player_names = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        player_names.append(name)

    game = GameController(player_names)
    game.play_game()

if __name__ == "__main__":
    main()
