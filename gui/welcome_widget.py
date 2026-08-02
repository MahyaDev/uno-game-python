from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal

class WelcomeWidget(QWidget):
    game_started = Signal(str, int)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(main_layout)

        self.title_label = QLabel("🃏 WELCOME TO UNO! 🃏")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        instruction_text = (
            "📌 HOW TO PLAY:\n"
            "  • Match cards by color or number\n"
            "  • Action cards: Skip, Reverse, Draw Two\n"
            "  • Wild cards: Change color or Draw Four\n"
            "  • First to empty their hand WINS! 🏆\n"
            "💡 Tip: Plan your moves wisely and use action cards strategically.\n\n"
            "Let the game begin! 🎮"
        )
        self.instruction_label = QLabel(instruction_text)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)

        main_layout.addStretch()

        name_layout = QHBoxLayout()
        name_layout.setSpacing(10)

        self.name_label = QLabel("What's your name?")
        self.name_label.setAlignment(Qt.AlignCenter)
        name_layout.addWidget(self.name_label, alignment=Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFixedWidth(200)
        self.name_input.setAlignment(Qt.AlignCenter)
        name_layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        main_layout.addLayout(name_layout)

        opponent_layout = QHBoxLayout()
        opponent_layout.setSpacing(10)

        self.opponents_label = QLabel("How many opponents do you want?")
        self.opponents_label.setAlignment(Qt.AlignCenter)
        opponent_layout.addWidget(self.opponents_label, alignment=Qt.AlignCenter)

        self.opponents_spinbox = QSpinBox()
        self.opponents_spinbox.setRange(1, 9)
        self.opponents_spinbox.setValue(2)
        self.opponents_spinbox.setSuffix(" opponent(s)")
        self.opponents_spinbox.setFixedWidth(150)
        self.opponents_spinbox.setAlignment(Qt.AlignCenter)
        opponent_layout.addWidget(self.opponents_spinbox, alignment=Qt.AlignCenter)

        main_layout.addLayout(opponent_layout)

        main_layout.addStretch()

        self.start_button = QPushButton("Start Game")
        self.start_button.setFixedWidth(150)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.connect_signals()

    def connect_signals(self):
        self.start_button.clicked.connect(self.start_game)

    def start_game(self):
        user_name = self.name_input.text().strip()
        opponent_count = self.opponents_spinbox.value()

        if not user_name:
            QMessageBox.warning(
                self,
                "Invalid Name",
                "Name cannot be only spaces."
            )
            return

        self.game_started.emit(user_name, opponent_count)
