import pytest
from src.models.player import Player
from src.models.card import Card, Suit, Rank


def test_player_creation():
    player = Player("Test Player")
    assert player.name == "Test Player"
    assert len(player.hand) == 0
    assert len(player.tricks_won) == 0


def test_receive_cards():
    player = Player("Test Player")
    cards = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)]
    player.add_cards(cards)
    assert len(player.hand) == 2
    assert player.hand == cards


def test_play_card():
    player = Player("Test Player")
    card = Card(Suit.HEARTS, Rank.ACE)
    player.add_cards([card])

    played = player.remove_card(card)
    assert played == card
    assert len(player.hand) == 0


def test_play_invalid_card():
    player = Player("Test Player")
    card = Card(Suit.HEARTS, Rank.ACE)
    with pytest.raises(ValueError):
        player.remove_card(card)


def test_win_trick():
    player = Player("Test Player")
    trick = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)]
    player.win_trick(trick)
    assert len(player.tricks_won) == 1
    assert player.tricks_won[0] == trick
