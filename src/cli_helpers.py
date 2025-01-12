from typing import Dict, List, Tuple
from src.models.game_round import GameRound
from src.models.player import Player
from src.models.card import Card

def print_hand(round: GameRound, player: Player) -> Tuple[Dict[int, int], List[Card]]:
    """Print cards vertically, numbering only valid plays."""
    print("Your hand:")
    playable_indices = {}
    index = 0
    hand = round.get_hand(player)

    for i, card in enumerate(hand):
        prefix = "  "
        if round.check_play_validity(player, card) is None:
            prefix = f"[{index}]"
            playable_indices[index] = i
            index += 1
        print(f"{prefix} {card}")
    return playable_indices, hand

def get_card_choice(playable_indices: Dict[int, int], hand: List[Card]) -> Card:
    """Get valid card selection from user."""
    while True:
        try:
            choice = int(input("Choose a card (number): "))
            if choice in playable_indices:
                return hand[playable_indices[choice]]
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def get_bids(players, num_tricks) -> Dict[Player, int]:
    """Get bids from all players for a round."""
    bids = {}
    total_bid = 0
    print(f"\nEnter bids (0-{num_tricks})")

    for i, player in enumerate(players):
        while True:
            try:
                remaining = num_tricks - total_bid
                if i == len(players) - 1:
                    print(f"Cannot bid {remaining}")
                bid = int(input(f"{player.name}'s bid: "))
                if bid < 0 or bid > num_tricks:
                    print(f"Bid must be between 0 and {num_tricks}")
                    continue
                if i == len(players) - 1 and bid == remaining:
                    print("Last player cannot make bids sum to total tricks")
                    continue
                bids[player] = bid
                total_bid += bid
                break
            except ValueError:
                print("Please enter a number")

    return bids

def play_round_loop(round: GameRound) -> None:
    """Main game loop for playing a single round."""
    current_player_idx = 0

    if round.trump_suit:
        print(f"\nTrump suit for this round: {Card._suit_symbols[round.trump_suit]}")

    while not round.is_over():
        print("\n" + "=" * 40)
        current_player = round.players[current_player_idx]
        print(f"\nCurrent player: {current_player.name}")

        if round.trump_suit:
            print(f"Trump suit: {Card._suit_symbols[round.trump_suit]}")

        if round.current_trick:
            print("\nCurrent trick:")
            for played_card in round.current_trick:
                print(f"{played_card.player.name}: {played_card.card}")

        while True:
            playable_indices, hand = print_hand(round, current_player)
            if not playable_indices:
                print("No playable cards!")
                break
            card = get_card_choice(playable_indices, hand)
            error = round.check_play_validity(current_player, card)
            if error is None:
                round.play_card(current_player, card)
                break
            print(f"Invalid play: {error}")

        if len(round.current_trick) == len(round.players):
            print("\nCompleted trick:")
            for played_card in round.current_trick:
                print(f"{played_card.player.name}: {played_card.card}")
            print()
            try:
                winner = round.evaluate_trick()
                print(f"\n{winner.name} wins the trick!")
                current_player_idx = round.players.index(winner)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            current_player_idx = (current_player_idx + 1) % len(round.players)
