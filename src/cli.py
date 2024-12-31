from .models.player import Player
from .models.game_round import GameRound
from .models.card import Card
from .models.deck import Deck


def print_hand(hand, round: GameRound, player: Player):
    """Print cards vertically, numbering only valid plays."""
    print("Your hand:")
    playable_indices = {}
    index = 0

    for i, card in enumerate(hand):
        prefix = "  "
        if round.check_play_validity(player, card) is None:
            prefix = f"[{index}]"
            playable_indices[index] = i
            index += 1
        print(f"{prefix} {card}")
    return playable_indices


def get_card_choice(hand, playable_indices):
    """Get valid card selection from user."""
    while True:
        try:
            choice = int(input("Choose a card (number): "))
            if choice in playable_indices:
                return hand[playable_indices[choice]]
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")


def main():
    # Game setup
    print("Playing a test round of Gulk.")
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

    round = GameRound(player_names)

    # Ask about trump suits
    while True:
        trump_choice = input("Use trump suits? (y/n): ").lower()
        if trump_choice in ["y", "n"]:
            use_trump = trump_choice == "y"
            break
        print("Please enter 'y' or 'n'.")

    # Ask for number of cards
    while True:
        try:
            max_cards = (Deck.STANDARD_DECK_SIZE - 1) // len(
                round.players
            )  # Account for trump card
            cards_per_player = int(
                input(f"Enter number of cards per player (1-{max_cards}): ")
            )
            if 1 <= cards_per_player <= max_cards:
                break
            print(f"Please enter a number between 1 and {max_cards}.")
        except ValueError:
            print("Please enter a valid number.")

    round.setup_round(cards_per_player, trump=use_trump)

    if round.trump_suit:
        print(f"\nTrump suit for this round: {Card._suit_symbols[round.trump_suit]}")

    # Game loop
    current_player_idx = 0
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
            playable_indices = print_hand(current_player.hand, round, current_player)
            if not playable_indices:
                print("No playable cards!")
                break
            card = get_card_choice(current_player.hand, playable_indices)
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

    # Game end
    print("\nRound Over!")
    for player in round.players:
        print(f"{player.name}: {len(player.tricks_won)} tricks")


if __name__ == "__main__":
    main()
