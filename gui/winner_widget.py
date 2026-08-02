from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtCore import Qt, Signal
from uno.player import Player
import random

class WinnerWidget(QWidget):
    yes_clicked = Signal()
    no_clicked = Signal()

    WIN_QUESTIONS = [
        "My hand's itching for another +2... you in?",
        "One more round or call it a night?",
        "Ready for a rematch? I'm sure you won't get that lucky twice!",
        "I still have a +4 with your name on it... wanna go again?",
        "Uno again? This time no mercy!"
    ]

    LOSE_QUESTIONS = [
        "Again? Ready to lose twice in a row? 😏",
        "If you dare, let's have a rematch!",
        "Shall we call it quits? Or one more UNO más?",
        "I wanna see if you can handle another +4!",
        "I'm on a roll — care to be my victim one more time?"
    ]

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)

        self.main_layout.addStretch()

        self.winner_label = QLabel()
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.winner_label, alignment=Qt.AlignCenter)

        self.main_layout.addStretch()

        self.play_again_label = QLabel()
        self.play_again_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.play_again_label, alignment=Qt.AlignCenter)

        self.button_row = QHBoxLayout()
        self.button_row.setSpacing(20)

        self.yes_btn = QPushButton("✔ Yes")
        self.yes_btn.setFixedWidth(100)
        self.yes_btn.clicked.connect(lambda checked: self.yes_clicked.emit())

        self.no_btn = QPushButton("✘ No")
        self.no_btn.setFixedWidth(100)
        self.no_btn.clicked.connect(lambda checked: self.no_clicked.emit())

        self.button_row.addStretch()

        self.button_row.addWidget(self.yes_btn, alignment=Qt.AlignCenter)
        self.button_row.addWidget(self.no_btn, alignment=Qt.AlignCenter)

        self.button_row.addStretch()

        self.main_layout.addLayout(self.button_row)

    def set_winner(self, winner: Player) -> None:
        self.winner = winner
        self.winner_label.setText(f"🎉 {winner.name} won! 🎉")

        self.show_question()

    def show_question(self) -> None:
        if self.winner.needs_external_input:
            self.play_again_label.setText(random.choice(self.WIN_QUESTIONS))
        else:
            self.play_again_label.setText(random.choice(self.LOSE_QUESTIONS))
