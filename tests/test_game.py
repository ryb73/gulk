import pytest
from src.models.deck import Deck
from src.models.game import TrickTakingGame, PlayedCard
from src.models.card import Card, Suit, Rank


def test_game_creation():
    game = TrickTakingGame(["Player 1", "Player 2"])
    assert len(game.players) == 2
    assert len(game.current_trick) == 0


def test_game_setup():
    game = TrickTakingGame(["Player 1", "Player 2"])
    game.setup_round(5)  # Deal 5 cards to each player
    assert len(game.players[0].hand) == 5
    assert len(game.players[1].hand) == 5
    assert len(game.current_trick) == 0


def test_invalid_cards_per_player():
    game = TrickTakingGame(["Player 1", "Player 2"])
    with pytest.raises(ValueError):
        game.setup_round(0)  # Too few cards
    with pytest.raises(ValueError):
        game.setup_round(27)  # Too many cards (deck has 52 cards)


def test_must_follow_suit():
    game = TrickTakingGame(["Player 1", "Player 2"])
    player = game.players[0]

    # Give player some cards
    hearts = Card(Suit.HEARTS, Rank.ACE)
    spades = Card(Suit.SPADES, Rank.ACE)
    player.add_cards([hearts, spades])

    # Lead a heart
    leading_card = Card(Suit.HEARTS, Rank.TWO)
    game.current_trick = [PlayedCard(leading_card, game.players[1])]

    # Shouldn't be able to play spade
    result = game.can_play_card(player, spades)
    assert isinstance(result, str)
    assert "Must follow suit" in result

    # Should be able to play heart
    assert game.can_play_card(player, hearts) is True


def test_complete_trick_error():
    game = TrickTakingGame(["Player 1", "Player 2"])
    player = game.players[0]
    card = Card(Suit.HEARTS, Rank.ACE)

    # Fill the trick
    game.current_trick = [
        PlayedCard(Card(Suit.HEARTS, Rank.TWO), p) for p in game.players
    ]

    result = game.can_play_card(player, card)
    assert isinstance(result, str)
    assert "Trick is already complete" in result


def test_trick_evaluation():
    game = TrickTakingGame(["Player 1", "Player 2"])
    player1, player2 = game.players

    # Player 1 plays high card
    high_card = Card(Suit.HEARTS, Rank.ACE)
    low_card = Card(Suit.HEARTS, Rank.TWO)

    player1.add_cards([high_card])
    player2.add_cards([low_card])

    game.play_card(player1, high_card)
    game.play_card(player2, low_card)

    winner = game.evaluate_trick()
    assert winner == player1
    assert len(player1.tricks_won) == 1


def test_trump_disabled():
    game = TrickTakingGame(["Player 1", "Player 2"])
    game.setup_round(5, trump=False)
    assert game.trump_suit is None


def test_trump_enabled():
    game = TrickTakingGame(["Player 1", "Player 2"])
    game.setup_round(5, trump=True)
    assert game.trump_suit is not None
    assert game.trump_suit in list(Suit)


def create_test_deck(*cards: Card) -> Deck:
    """Create a deck with specific cards in a specific order."""
    deck = Deck()
    deck.cards = list(cards)
    return deck


def test_trump_card_wins():
    # Create specific cards for the test
    spade_ace = Card(Suit.SPADES, Rank.ACE)
    heart_two = Card(Suit.HEARTS, Rank.TWO)
    heart_three = Card(Suit.HEARTS, Rank.THREE)  # Will be trump card

    # Create deck with exactly the cards we need
    deck = create_test_deck(spade_ace, heart_two, heart_three)

    # Create game with test deck
    game = TrickTakingGame(["Player 1", "Player 2"], deck=deck)
    game.setup_round(1, trump=True)  # Deal 1 card to each player

    player1, player2 = game.players

    assert game.trump_suit == Suit.HEARTS
    assert spade_ace in player1.hand
    assert heart_two in player2.hand

    game.play_card(player1, spade_ace)
    game.play_card(player2, heart_two)

    winner = game.evaluate_trick()
    assert winner == player2  # Trump wins even against high card
