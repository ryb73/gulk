import pytest
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
    assert not game.can_play_card(player, spades)

    # Should be able to play heart
    assert game.can_play_card(player, hearts)


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
