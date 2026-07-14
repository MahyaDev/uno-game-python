from .card import (
    CardColor,
    NumberCard,
    ActionCard,
    WildCard,
    ActionCardValue,
    WildCardValue
)
import random

class Deck:
    def __init__(self):
        self.draw_pile = self.create_deck()
        self.discard_pile = []

    def create_deck(self):
        draw_pile = []

        repeat_count = {
            "number_zero": 1,
            "number_1_9": 2,
            "action": 2,
            "wild": 4
        }

        for color in CardColor:
            draw_pile.extend(
                NumberCard(color, 0)
                for _ in range(repeat_count["number_zero"])
            )

            for number in range(1, 10):
                draw_pile.extend(
                    NumberCard(color, number)
                    for _ in range(repeat_count["number_1_9"])
                )

        for color in CardColor:
            for value in ActionCardValue:
                draw_pile.extend(
                    ActionCard(color, value)
                    for _ in range(repeat_count["action"])
                )

        for value in WildCardValue:
            draw_pile.extend(
                WildCard(value)
                for _ in range(repeat_count["wild"])
            )

        return draw_pile
    
    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw_card(self):
        if not self.draw_pile:
            self.recycle_discard()
        return self.draw_pile.pop()
    
    def discard(self, played_card):
        self.discard_pile.append(played_card)

    def recycle_discard(self):
        if len(self.discard_pile) <= 1:
            return

        top_card = self.discard_pile.pop()

        for card in self.discard_pile:
            if isinstance(card, WildCard):
                card.color = None

        self.draw_pile.extend(self.discard_pile)
        self.discard_pile.clear()
        self.discard_pile.append(top_card)

        self.shuffle()
