from .card import (
    Card,
    ActionCard,
    WildCard,
    ActionCardValue,
    WildCardValue
)
from .deck import Deck
from .player import Player

class Game:
    MIN_PLAYERS = 2
    MAX_PLAYERS = 10

    def __init__(self, deck: Deck, players: list[Player]):
        self._validate_players(players)
        self.deck = deck
        self.players = players
        self.current_player_index = 0
        self.direction = 1
        self.is_running = True

    @property
    def current_card(self):
        return self.deck.discard_pile[-1]

    def _validate_players(self, players):
        if not all(isinstance(player, Player) for player in players):
            raise TypeError("All players must be Player instances")

        if not self.MIN_PLAYERS <= len(players) <= self.MAX_PLAYERS:
            raise ValueError("Players must be between 2 and 10")
        
        names = [player.name for player in players]

        if len(names) != len(set(names)):
            raise ValueError("Player names must be unique")

    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def get_next_player_index(self):
        return (self.current_player_index + self.direction) % len(self.players)

    def apply_card_effect(self, card: Card):
        if isinstance(card, ActionCard):
            if card.value == ActionCardValue.REVERSE:
                if len(self.players) == 2:
                    self.next_turn()
                else:
                    self.direction *= -1
            
            elif card.value == ActionCardValue.SKIP:
                self.next_turn()
            
            elif card.value == ActionCardValue.DRAW_TWO:
                next_player = self.get_next_player_index()
                self.players[next_player].draw_card(self.deck, 2)
                # Skip the player who drew two cards
                self.next_turn()
        
        if isinstance(card, WildCard):
            if card.value == WildCardValue.WILD:
                chosen_color = self.players[self.current_player_index].choose_color()
                card.color = chosen_color
            
            elif card.value == WildCardValue.WILD_DRAW_FOUR:
                next_player = self.get_next_player_index()
                self.players[next_player].draw_card(self.deck, 4)

                chosen_color = self.players[self.current_player_index].choose_color()
                card.color = chosen_color
                # Skip the player who drew four cards
                self.next_turn()

    def process_turn(self):
        player = self.players[self.current_player_index]
        playable_cards = player.get_playable_cards(self.current_card)

        if not playable_cards:
            print(f"{player.name} has no playable card. Drawing a card...")
            drawn_card = player.draw_card(self.deck, 1)

            if not drawn_card.is_playable(self.current_card):
                print(f"{player.name} drew a card but it's not playable. Turn passes.")
                self.next_turn()
                return
            
            print(f"{player.name} drew a playable card and will play it!")
            chosen_card = drawn_card
        
        else:
            chosen_card = player.choose_card(playable_cards)

        player.play_card(chosen_card)
        self.deck.discard(chosen_card)
        self.apply_card_effect(chosen_card)

        if len(player.hand) == 0:
            print(f"{player.name} won! 🎉")
            self.is_running = False
            return
        
        if len(player.hand) == 1:
            player.call_uno()

        self.next_turn()
