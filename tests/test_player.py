from src.models.player import Player


def test_player_creation():
    player = Player("Test Player")
    assert player.name == "Test Player"
