from .models.game import TrickTakingGame
from .models.card import Card


def print_hand(hand):
    """Print cards with their index for selection."""
    print("Your hand:")
    for i, card in enumerate(hand):
        print(f"[{i}] {card}", end="  ")
    print()


def get_card_choice(hand):
    """Get valid card selection from user."""
    while True:
        try:
            choice = int(input("Choose a card (number): "))
            if 0 <= choice < len(hand):
                return hand[choice]
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
    game.setup_round()

    # Game loop
    current_player_idx = 0
    while len(game.players[0].hand) > 0:
        print("\n" + "=" * 40)
        current_player = game.players[current_player_idx]
        print(f"\nCurrent player: {current_player.name}")

        if game.current_trick:
            print("\nCurrent trick:")
            for card in game.current_trick:
                print(card, end="  ")
            print()

        print_hand(current_player.hand)

        while True:
            card = get_card_choice(current_player.hand)
            if game.can_play_card(current_player, card):
                break
            print("Invalid play. You must follow suit if possible.")

        if len(game.current_trick) == len(game.players):
            winner = game.evaluate_trick()
            print(f"\n{winner.name} wins the trick!")
            current_player_idx = game.players.index(winner)
        else:
            current_player_idx = (current_player_idx + 1) % len(game.players)

    # Game end
    print("\nGame Over!")
    for player in game.players:
        print(f"{player.name}: {len(player.tricks_won)} tricks")


if __name__ == "__main__":
    main()
