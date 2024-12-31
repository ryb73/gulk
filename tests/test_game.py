import pytest
from src.models.deck import Deck
from src.models.game_round import GameRound, PlayedCard
from src.models.card import Card, Suit, Rank


def test_round_creation():
    round = GameRound(["Player 1", "Player 2"])
    assert len(round.players) == 2
    assert len(round.current_trick) == 0


def test_round_setup():
    round = GameRound(["Player 1", "Player 2"])
    round.setup_round(5)  # Deal 5 cards to each player
    assert len(round.players[0].hand) == 5
    assert len(round.players[1].hand) == 5
    assert len(round.current_trick) == 0


def test_invalid_cards_per_player():
    round = GameRound(["Player 1", "Player 2"])
    with pytest.raises(ValueError):
        round.setup_round(0)  # Too few cards
    with pytest.raises(ValueError):
        round.setup_round(27)  # Too many cards (deck has 52 cards)


def test_must_follow_suit():
    round = GameRound(["Player 1", "Player 2"])
    player = round.players[0]

    # Give player some cards
    hearts = Card(Suit.HEARTS, Rank.ACE)
    spades = Card(Suit.SPADES, Rank.ACE)
    player.add_cards([hearts, spades])

    # Lead a heart
    leading_card = Card(Suit.HEARTS, Rank.TWO)
    round.current_trick = [PlayedCard(leading_card, round.players[1])]

    # Shouldn't be able to play spade
    result = round.check_play_validity(player, spades)
    assert isinstance(result, str)
    assert "Must follow suit" in result

    # Should be able to play heart
    assert round.check_play_validity(player, hearts) is None


def test_complete_trick_error():
    round = GameRound(["Player 1", "Player 2"])
    player = round.players[0]
    card = Card(Suit.HEARTS, Rank.ACE)

    # Fill the trick
    round.current_trick = [
        PlayedCard(Card(Suit.HEARTS, Rank.TWO), p) for p in round.players
    ]

    result = round.check_play_validity(player, card)
    assert isinstance(result, str)
    assert "Trick is already complete" in result


def test_trick_evaluation():
    round = GameRound(["Player 1", "Player 2"])
    player1, player2 = round.players

    # Player 1 plays high card
    high_card = Card(Suit.HEARTS, Rank.ACE)
    low_card = Card(Suit.HEARTS, Rank.TWO)

    player1.add_cards([high_card])
    player2.add_cards([low_card])

    round.play_card(player1, high_card)
    round.play_card(player2, low_card)

    winner = round.evaluate_trick()
    assert winner == player1
    assert len(player1.tricks_won) == 1


def test_trump_disabled():
    round = GameRound(["Player 1", "Player 2"])
    round.setup_round(5, trump=False)
    assert round.trump_suit is None


def test_trump_enabled():
    round = GameRound(["Player 1", "Player 2"])
    round.setup_round(5, trump=True)
    assert round.trump_suit is not None
    assert round.trump_suit in list(Suit)


def create_test_deck(*cards: Card) -> Deck:
    """Create a deck with specific cards in a specific order."""
    return Deck(cards)


def test_trump_card_wins():
    # Create specific cards for the test
    heart_three = Card(Suit.HEARTS, Rank.THREE)  # Will be trump card
    heart_two = Card(Suit.HEARTS, Rank.TWO)
    spade_ace = Card(Suit.SPADES, Rank.ACE)

    # Create deck with exactly the cards we need
    deck = create_test_deck(heart_three, heart_two, spade_ace)

    # Create round with test deck
    round = GameRound(["Player 1", "Player 2"])
    round.setup_round(1, trump=True, deck=deck)  # Pass deck during setup

    player1, player2 = round.players

    assert round.trump_suit == Suit.HEARTS
    assert spade_ace in player1.hand
    assert heart_two in player2.hand

    round.play_card(player1, spade_ace)
    round.play_card(player2, heart_two)

    winner = round.evaluate_trick()
    assert winner == player2  # Trump wins even against high card
