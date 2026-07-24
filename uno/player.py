from .card import (
    Card,
    CardColor,
    WildCard,
    ActionCard,
    NumberCard,
    WildCardValue
)
from .deck import Deck
import random

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
        if not isinstance(entry, str):
            raise TypeError("Name must be str")
        
        entry = entry.strip()

        if not entry:
            raise ValueError("Name cannot be empty or contain only spaces")
        
        self._name = entry

    def get_playable_cards(self, current_card: Card) -> list[Card]:
        return [
            card for card in self.hand
            if card.is_playable(current_card)
        ]

    def choose_card(self, playable_cards: list[Card], current_card: Card) -> Card:
        print("Your hand:")

        for card in self.hand:
            print(card)

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

    def play_card(self, card: Card) -> Card:
        self.hand.remove(card)
        return card

    def choose_color(self) -> CardColor:
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

    def call_uno(self) -> None:
        if len(self.hand) == 1:
            print("UNO! 🎯")

class BotPlayer(Player):
    NUMBER_CARD_SCORE = 10
    ACTION_CARD_SCORE = 5
    WILD_CARD_PENALTY = -10

    COLOR_MATCH_SCORE = 30
    VALUE_MATCH_SCORE = 30

    DOMINANT_COLOR_HIGH_BONUS = 15
    DOMINANT_COLOR_MEDIUM_BONUS = 10

    DUPLICATE_CARD_BONUS = 5
    SINGLE_ACTION_PENALTY = -5

    LATE_GAME_WILD_BONUS = 30
    LATE_GAME_DRAW4_BONUS = 35

    def choose_card(self, playable_cards: list[Card], current_card: Card) -> Card:
        dominant_colors = self.get_dominant_colors()

        best_cards = []
        best_score = -float('inf')

        for card in playable_cards:
            score = self.calculate_strategic_score(card, current_card, dominant_colors)
            
            if score > best_score:
                best_score = score
                best_cards = [card]
            elif score == best_score:
                best_cards.append(card)

        return random.choice(best_cards)
    
    def choose_color(self) -> CardColor:
        dominant_colors = self.get_dominant_colors()
        
        if not dominant_colors:
            return random.choice(list(CardColor))

        best_colors = []
        max_count = 0

        for color, count in dominant_colors.items():
            if count > max_count:
                max_count = count
                best_colors = [color]
            elif count == max_count:
                best_colors.append(color)
        
        return random.choice(best_colors)
    
    def calculate_strategic_score(self, card: Card, current_card: Card, dominant_colors: dict[CardColor, int]) -> int:
        score = 0

        score += self.calculate_card_type_score(card)
        score += self.calculate_matching_score(card, current_card)
        score += self.calculate_dominant_color_score(card, dominant_colors)
        score += self.calculate_duplicate_score(card)
        score += self.calculate_late_game_score(card)

        return score

    def calculate_card_type_score(self, card: Card) -> int:
        score = 0

        if isinstance(card, WildCard):
            score += self.WILD_CARD_PENALTY

        elif isinstance(card, ActionCard):
            score += self.ACTION_CARD_SCORE

        elif isinstance(card, NumberCard):
            score += self.NUMBER_CARD_SCORE

        return score

    def calculate_matching_score(self, card: Card, current_card: Card) -> int:
        score = 0

        if current_card:
            if card.color == current_card.color:
                score += self.COLOR_MATCH_SCORE
            if card.value == current_card.value:
                score += self.VALUE_MATCH_SCORE

        return score

    def calculate_dominant_color_score(self, card: Card, dominant_colors: dict[CardColor, int]) -> int:
        score = 0
        
        count = dominant_colors.get(card.color, 0)

        if count >= 3:
            score += self.DOMINANT_COLOR_HIGH_BONUS
        elif count == 2:
            score += self.DOMINANT_COLOR_MEDIUM_BONUS

        return score

    def calculate_duplicate_score(self, card: Card) -> int:
        score = 0

        count = self.count_same_values(card.value)

        if isinstance(card, ActionCard):
            if count >= 2:
                score += self.DUPLICATE_CARD_BONUS
            else:
                score += self.SINGLE_ACTION_PENALTY

        elif isinstance(card, NumberCard):
            if count >= 2:
                score += self.DUPLICATE_CARD_BONUS

        return score

    def calculate_late_game_score(self, card: Card) -> int:
        score = 0

        if not isinstance(card, WildCard):
            return 0

        if len(self.hand) == 3:
            score += self.LATE_GAME_WILD_BONUS
        elif len(self.hand) == 2:
            if card.value == WildCardValue.WILD:
                score += self.LATE_GAME_WILD_BONUS
            elif card.value == WildCardValue.WILD_DRAW_FOUR:
                score += self.LATE_GAME_DRAW4_BONUS

        return score
        
    def count_same_values(self, value) -> int:
        return sum(
            c.value == value
            for c in self.hand
        )

    def get_dominant_colors(self) -> dict[CardColor, int]:
        color_count = {}

        for card in self.hand:
            if card.color is not None:
                color_count[card.color] = color_count.get(card.color, 0) + 1
        
        return color_count
