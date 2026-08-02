from PySide6.QtWidgets import QMainWindow, QStackedWidget
from .welcome_widget import WelcomeWidget
from .game_widget import GameWidget
from .winner_widget import WinnerWidget
from .game_controller import GameController
from uno.card import WildCard
from uno.deck import Deck
from uno.player import Player
from uno.game import Game
from uno.game_setup import create_players

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UNO Game")
        self.resize(1000, 500)

        self.stack = QStackedWidget()

        self.setCentralWidget(self.stack)

        self.welcome_widget = WelcomeWidget()
        self.game_widget = GameWidget()
        self.winner_widget = WinnerWidget()

        self.stack.addWidget(self.welcome_widget)
        self.stack.addWidget(self.game_widget)
        self.stack.addWidget(self.winner_widget)

        self.welcome_widget.game_started.connect(self.on_game_started)

        self.winner_widget.yes_clicked.connect(self.on_play_again)
        self.winner_widget.no_clicked.connect(self.on_not_play_again)

    def on_game_started(self, name: str, bot_count: int) -> None:
        self.game_widget.reset()

        deck = Deck()

        players = create_players(deck, name, bot_count)

        self.game = Game(deck, players)

        starting_card = deck.draw_card()
    
        while isinstance(starting_card, WildCard):
            deck.draw_pile.insert(0, starting_card)
            starting_card = deck.draw_card()
    
        deck.discard(starting_card)

        self.controller = GameController(self.game, self.game_widget)
        self.controller.game_over.connect(self.on_game_over)

        self.stack.setCurrentWidget(self.game_widget)

        self.controller.run_turn()

    def on_game_over(self, winner: Player) -> None:
        self.winner_widget.set_winner(winner)
        self.stack.setCurrentWidget(self.winner_widget)

    def on_play_again(self) -> None:
        self.stack.setCurrentWidget(self.welcome_widget)

    def on_not_play_again(self) -> None:
        self.close()
