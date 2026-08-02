import random
from .deck import Deck
from .player import Player, BotPlayer, HumanPlayer

def create_players(deck: Deck, player_name: str, bot_count: int) -> list[Player]:
    players = []

    players.append(HumanPlayer(deck, player_name))

    for i in range(bot_count):
        players.append(BotPlayer(deck, f"Bot {i+1}"))

    random.shuffle(players)

    return players
