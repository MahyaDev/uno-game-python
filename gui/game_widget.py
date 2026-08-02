from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget
)
from PySide6.QtCore import Qt, Signal
from uno.card import Card, CardColor, WildCard
from uno.player import Player

class GameWidget(QWidget):
    card_selected = Signal(object)
    color_selected = Signal(object)

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(30)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)

        self.main_layout.addStretch()

        self.current_player_label = QLabel()
        self.current_card_label = QLabel()
        self.main_layout.addWidget(self.current_player_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.current_card_label, alignment=Qt.AlignCenter)

        self.hand_label = QLabel("Your hand:")
        self.main_layout.addWidget(self.hand_label, alignment=Qt.AlignCenter)

        self.hand_layout = QHBoxLayout()
        self.main_layout.addLayout(self.hand_layout)

        self.color_label = QLabel("Choose a color:")
        self.main_layout.addWidget(self.color_label, alignment=Qt.AlignCenter)

        self.color_layout = QHBoxLayout()
        self.main_layout.addLayout(self.color_layout)

        self.build_color_button()
        self.hide_color_picker()

        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)

        message_column = QVBoxLayout()

        self.message_log_title = QLabel("Message Log:")
        message_column.addWidget(self.message_log_title, alignment=Qt.AlignCenter)

        self.message_log = QListWidget()
        message_column.addWidget(self.message_log, alignment=Qt.AlignCenter)

        self.bottom_layout.addLayout(message_column)

        hand_sizes_column = QVBoxLayout()

        self.hand_sizes_title = QLabel("Hand Sizes Summary:")
        hand_sizes_column.addWidget(self.hand_sizes_title, alignment=Qt.AlignCenter)

        self.hand_sizes_label = QLabel()
        hand_sizes_column.addWidget(self.hand_sizes_label, alignment=Qt.AlignCenter)

        self.bottom_layout.addLayout(hand_sizes_column)

        self.main_layout.addStretch()

    def reset(self) -> None:
        self.current_player_label.clear()
        self.current_card_label.clear()
        self.message_log.clear()
        self.hand_sizes_label.clear()
        self.hide_color_picker()

        while self.hand_layout.count():
            item = self.hand_layout.takeAt(0)
            item.widget().deleteLater()

    def update_state(self, player: Player, current_card: Card) -> None:
        self.current_player_label.setText(f"Current player: {player.name}")
        self.current_card_label.setText(f"Current card: {current_card}")

        playable_cards = player.get_playable_cards(current_card)

        self.rebuild_hand_buttons(player.hand, playable_cards)

    def card_style(self, card: Card, playable: bool) -> str:
        color_map = {
            CardColor.RED: "#e53935",
            CardColor.BLUE: "#1e88e5",
            CardColor.GREEN: "#43a047",
            CardColor.YELLOW: "#fdd835",
        }

        if isinstance(card, WildCard):
            background = "#424242"
            text = "white"
        else:
            background = color_map.get(card.color, "#757575")
            text = "black" if card.color == CardColor.YELLOW else "white"

        if not playable:
            background = "#bdbdbd"
            text = "#666666"

        return f"""
            QPushButton {{
                background-color: {background};
                color: {text};
                border: 2px solid black;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }}

            QPushButton:hover:enabled {{
                border: 3px solid white;
            }}

            QPushButton:pressed:enabled {{
                background-color: #222222;
            }}
        """

    def rebuild_hand_buttons(self, hand: list[Card], playable_cards: list[Card]) -> None:
        while self.hand_layout.count():
            item = self.hand_layout.takeAt(0)
            item.widget().deleteLater()

        self.hand_layout.setSpacing(12)

        for card in hand:
            playable = card in playable_cards

            text = str(card)

            text = (
                text.replace(" wild draw four", "\nwild\ndraw four")
                    .replace(" reverse", "\nreverse")
                    .replace(" draw two", "\ndraw two")
            )

            button = QPushButton(text)
            button.setFixedSize(90, 120)
            button.setEnabled(playable)
            button.setStyleSheet(self.card_style(card, playable))

            button.clicked.connect(lambda checked, card=card: self.card_selected.emit(card))

            self.hand_layout.addWidget(button)

    def color_button_style(self, color: CardColor) -> str:
        color_map = {
            CardColor.RED: ("#e53935", "white"),
            CardColor.BLUE: ("#1e88e5", "white"),
            CardColor.GREEN: ("#43a047", "white"),
            CardColor.YELLOW: ("#fdd835", "black"),
        }

        background, text = color_map[color]

        return f"""
            QPushButton {{
                background-color: {background};
                color: {text};
                border: 2px solid black;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }}

            QPushButton:hover {{
                border: 3px solid white;
            }}

            QPushButton:pressed {{
                background-color: #222222;
            }}
        """

    def build_color_button(self) -> None:
        self.color_layout.setSpacing(12)

        for color in CardColor:
            button = QPushButton(f"{color.emoji}\n{color.name}")
            button.setFixedSize(90, 80)
            button.setStyleSheet(self.color_button_style(color))

            button.clicked.connect(lambda checked, color=color: self.color_selected.emit(color))

            self.color_layout.addWidget(button)

    def show_color_picker(self) -> None:
        self.color_label.show()
        for i in range(self.color_layout.count()):
            self.color_layout.itemAt(i).widget().show()

    def hide_color_picker(self) -> None:
        self.color_label.hide()
        for i in range(self.color_layout.count()):
            self.color_layout.itemAt(i).widget().hide()

    def update_hand_sizes(self, summary: list[str]) -> None:
        self.hand_sizes_label.setText("\n".join(summary))

    def show_messages(self, messages: list[str]) -> None:
        for message in messages:
            self.message_log.addItem(message)

        self.message_log.scrollToBottom()
        self.message_log.setFixedWidth(350)
