from .models.player import Player
from .models.game import TrickTakingGame
from .models.card import Card


def print_hand(hand, game: TrickTakingGame, player: Player):
    """Print cards vertically, numbering only valid plays."""
    print("Your hand:")
    playable_indices = {}
    index = 0

    for i, card in enumerate(hand):
        prefix = "  "
        if game.can_play_card(player, card):
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
    print("Welcome to the Trick-Taking Game!")
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

    game = TrickTakingGame(player_names)

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
            max_cards = (len(game.deck.cards) - 1) // len(
                game.players
            )  # Account for trump card
            cards_per_player = int(
                input(f"Enter number of cards per player (1-{max_cards}): ")
            )
            if 1 <= cards_per_player <= max_cards:
                break
            print(f"Please enter a number between 1 and {max_cards}.")
        except ValueError:
            print("Please enter a valid number.")

    game.setup_round(cards_per_player, trump=use_trump)

    if game.trump_suit:
        print(f"\nTrump suit for this round: {Card._suit_symbols[game.trump_suit]}")

    # Game loop
    current_player_idx = 0
    while len(game.players[0].hand) > 0:
        print("\n" + "=" * 40)
        current_player = game.players[current_player_idx]
        print(f"\nCurrent player: {current_player.name}")

        if game.trump_suit:
            print(f"Trump suit: {Card._suit_symbols[game.trump_suit]}")

        if game.current_trick:
            print("\nCurrent trick:")
            for played_card in game.current_trick:
                print(f"{played_card.player.name}: {played_card.card}")

        while True:
            playable_indices = print_hand(current_player.hand, game, current_player)
            if not playable_indices:
                print("No playable cards!")
                break
            card = get_card_choice(current_player.hand, playable_indices)
            result = game.can_play_card(current_player, card)
            if result is True:
                game.play_card(current_player, card)
                break
            print(f"Invalid play: {result}")

        if len(game.current_trick) == len(game.players):
            print("\nCompleted trick:")
            for played_card in game.current_trick:
                print(f"{played_card.player.name}: {played_card.card}")
            print()
            try:
                winner = game.evaluate_trick()
                print(f"\n{winner.name} wins the trick!")
                current_player_idx = game.players.index(winner)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            current_player_idx = (current_player_idx + 1) % len(game.players)

    # Game end
    print("\nGame Over!")
    for player in game.players:
        print(f"{player.name}: {len(player.tricks_won)} tricks")


if __name__ == "__main__":
    main()
