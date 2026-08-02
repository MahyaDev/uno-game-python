from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget
)
from PySide6.QtCore import Qt, Signal
from uno.card import Card, CardColor
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

    def rebuild_hand_buttons(self, hand: list[Card], playable_cards: list[Card]) -> None:
        while self.hand_layout.count():
            item = self.hand_layout.takeAt(0)
            item.widget().deleteLater()

        for card in hand:
            button = QPushButton(str(card))
            button.setEnabled(card in playable_cards)

            button.clicked.connect(lambda checked, card=card: self.card_selected.emit(card))

            self.hand_layout.addWidget(button)

    def build_color_button(self) -> None:
        for color in CardColor:
            button = QPushButton(f"{color.name} {color.emoji}")
            button.setFixedWidth(80)

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
