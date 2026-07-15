from .card import Card, CardColor
from .deck import Deck

STARTING_HAND_SIZE = 7

class Player:
    def __init__(self, deck: Deck, name: str):
        self.hand = [
            deck.draw_card()
            for _ in range(STARTING_HAND_SIZE)
        ]
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, entry: str):
        entry = entry.strip()

        if not isinstance(entry, str):
            raise ValueError("Name must be str")

        if not entry:
            raise ValueError("Name must contain some characters")
        
        self._name = entry

    def get_playable_cards(self, current_card: Card) -> list[Card]:
        return [
            card for card in self.hand
            if card.is_playable(current_card)
        ]

    def choose_card(self, playable_cards: list[Card]) -> Card:
        print("Playable cards:")
        for index, card in enumerate(playable_cards, 1):
            print(f"{index}. {card}")

        while True:
            try:
                choice = int(input("Choose a card: "))
                idx = choice - 1

                if 0 <= (idx) < len(playable_cards):
                    return playable_cards[idx]
                print("Invalid choice!")

            except ValueError:
                print("Invalid input! Please enter a number.")

    def play_card(self, card: Card):
        self.hand.remove(card)
        return card

    def choose_color(self):
        valid_colors = list(CardColor)

        print("Choose a color:")
        for index, color in enumerate(valid_colors, 1):
            print(f"{index}. {color.name} {color.emoji}")

        while True:
            try:
                choice = int(input("Enter your chosen color (1-4): "))
                idx = choice - 1

                if 0 <= idx < len(valid_colors):
                    return valid_colors[idx]
                print("Invalid choice! Please enter 1-4")

            except ValueError:
                print("Invalid input! Please enter a number.")

    def draw_card(self, deck: Deck, cards_to_draw: int = 1):
        new_cards = [deck.draw_card() for _ in range(cards_to_draw)]
        self.hand.extend(new_cards)

        if cards_to_draw == 1:
            return new_cards[0]
        
        return new_cards

    def call_uno(self):
        if len(self.hand) == 1:
            print("UNO! 🎯")
