from PySide6.QtCore import QObject, Signal
from uno.card import (
    Card,
    CardColor,
    WildCard
)
from uno.player import Player
from uno.game import Game
from .game_widget import GameWidget

class GameController(QObject):
    game_over = Signal(object)

    def __init__(self, game: Game, game_widget: GameWidget):
        super().__init__()

        self.game = game
        self.widget = game_widget
        self.pending_card = None

        self.widget.card_selected.connect(self.on_card_selected)
        self.widget.color_selected.connect(self.on_color_selected)

    def run_turn(self) -> None:
        player = self.game.current_player
        current_card = self.game.current_card

        self.widget.update_state(player, current_card)
        self.widget.update_hand_sizes(self.game.get_hand_summary())

        playable_cards, context = self.game.start_turn()

        if not playable_cards:
            drawn_card, messages = self.game.draw_and_check()

            self.widget.show_messages(messages)

            if drawn_card:
                self.handle_chosen_card(drawn_card, player)
            else:
                self.run_turn()

        else:
            if player.needs_external_input:
                return
            
            else:
                chosen_card = player.choose_card(playable_cards, context)
                self.handle_chosen_card(chosen_card, player)

    def handle_chosen_card(self, chosen_card: Card, player: Player) -> None:
        if isinstance(chosen_card, WildCard):
            if player.needs_external_input:
                self.pending_card = chosen_card
                self.widget.show_color_picker()
                return

            else:
                chosen_color = player.choose_color()

        else:
            chosen_color = None

        self.finish_turn(chosen_card, chosen_color)

    def finish_turn(self, chosen_card: Card, chosen_color: CardColor | None) -> None:
        player = self.game.current_player
        messages = self.game.play_turn(chosen_card, chosen_color)

        self.widget.hide_color_picker()
        self.widget.show_messages(messages)

        if self.game.is_running:
            self.run_turn()

        else:
            self.game_over.emit(player)

    def on_card_selected(self, card: Card) -> None:
        self.handle_chosen_card(card, self.game.current_player)

    def on_color_selected(self, color: CardColor) -> None:
        self.finish_turn(self.pending_card, color)
        self.pending_card = None
