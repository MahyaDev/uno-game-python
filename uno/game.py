from .card import (
    Card,
    CardColor,
    ActionCard,
    WildCard,
    ActionCardValue,
    WildCardValue
)
from .deck import Deck
from .player import Player
from .turn_context import TurnContext

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
    def current_card(self) -> Card:
        return self.deck.discard_pile[-1]

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _validate_players(self, players: list[Player]) -> None:
        if not all(isinstance(player, Player) for player in players):
            raise TypeError("All players must be Player instances")

        if not self.MIN_PLAYERS <= len(players) <= self.MAX_PLAYERS:
            raise ValueError("Players must be between 2 and 10")
        
        names = [player.name for player in players]

        if len(names) != len(set(names)):
            raise ValueError("Player names must be unique")

    def next_turn(self) -> None:
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def get_next_player_index(self) -> int:
        return (self.current_player_index + self.direction) % len(self.players)

    def get_hand_summary(self) -> list[str]:
        player = self.current_player
        summary = []

        for p in self.players:
            count = len(p.hand)
            prefix = "▶️" if p == player else ""

            if count == 1:
                summary.append(f"{prefix} {p.name}: 1 card, UNO! 🎯")
            else:
                summary.append(f"{prefix} {p.name}: {count} cards")

        return summary

    def start_turn(self) -> tuple[list[Card], TurnContext]:
        player = self.current_player

        playable_cards = player.get_playable_cards(self.current_card)

        context = TurnContext(
            current_card=self.current_card,
            next_player=self.players[self.get_next_player_index()]
        )

        return playable_cards, context

    def draw_and_check(self) -> tuple[Card | None, list[str]]:
        player = self.current_player
        messages = []

        messages.append(f"{player.name} has no playable card. Drawing a card...")
        drawn_card = player.draw_card(self.deck, 1)

        if not drawn_card.is_playable(self.current_card):
            messages.append(f"{player.name} drew a card but it's not playable. Turn passes.")
            self.next_turn()
            return None, messages

        messages.append(f"{player.name} drew a playable card and will play it!")

        return drawn_card, messages

    def play_turn(self, chosen_card: Card, chosen_color: CardColor) -> list[str]:
        player = self.current_player
        messages = []

        messages.append(f"{player.name} played {chosen_card}")

        player.play_card(chosen_card)
        self.deck.discard(chosen_card)

        messages.extend(self.apply_card_effect(chosen_card, chosen_color))

        if len(player.hand) == 0:
            messages.append(f"{player.name} won! 🎉")
            self.is_running = False
            return messages
                
        if player.call_uno():
            messages.append(f"{player.name} says UNO! 🎯")
        
        self.next_turn()

        return messages

    def apply_card_effect(self, card: Card, chosen_color: CardColor = None) -> list[str]:
        current_player = self.current_player
        messages = []

        if isinstance(card, ActionCard):
            if card.value == ActionCardValue.REVERSE:
                if len(self.players) == 2:
                    self.next_turn()
                else:
                    self.direction *= -1

                messages.append(f"🔄 Direction reversed!")

            elif card.value == ActionCardValue.SKIP:
                skipped_player = self.players[self.get_next_player_index()]

                messages.append(f"🚫 {skipped_player.name}'s turn skipped!")

                self.next_turn()
            
            elif card.value == ActionCardValue.DRAW_TWO:
                next_player = self.players[self.get_next_player_index()]
                next_player.draw_card(self.deck, 2)

                messages.append(f"{next_player.name} drew 2 cards and was skipped!")

                # Skip the player who drew two cards
                self.next_turn()
        
        elif isinstance(card, WildCard):
            if chosen_color is None:
                raise ValueError("Wild cards require a chosen_color before applying their effect")

            if card.value == WildCardValue.WILD:
                card.color = chosen_color
                messages.append(f"🎨 {current_player.name} chose {chosen_color.value}")
            
            elif card.value == WildCardValue.WILD_DRAW_FOUR:
                next_player = self.players[self.get_next_player_index()]
                next_player.draw_card(self.deck, 4)

                messages.append(f"{next_player.name} drew 4 cards and was skipped!")

                card.color = chosen_color

                messages.append(f"🎨 {current_player.name} chose {chosen_color.value}")

                # Skip the player who drew four cards
                self.next_turn()

        return messages
