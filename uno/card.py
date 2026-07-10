from abc import ABC, abstractmethod
from enum import Enum

class CardColor(Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"

    @property
    def emoji(self):
        return {
            CardColor.BLUE: "🟦",
            CardColor.GREEN: "🟩",
            CardColor.RED: "🟥",
            CardColor.YELLOW: "🟨"
        }[self]

class ActionCardValue(Enum):
    SKIP = "skip"
    REVERSE = "reverse"
    DRAW_TWO = "draw two"

class WildCardValue(Enum):
    WILD = "wild"
    WILD_DRAW_FOUR = "wild draw four"

class Card(ABC):
    def __init__(self, color: CardColor):
        self._color = None
        self.color = color

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, entry):
        if entry is None:
            if not isinstance(self, WildCard):
                raise ValueError("Only WildCard can have no color")
            self._color = None
            return
        
        if not isinstance(entry, CardColor):
            raise ValueError("Color must be CardColor enum")
        
        self._color = entry

    def __str__(self):
        color = self.color.emoji if self.color else "🃏"

        if isinstance(self.value, Enum):
            value = self.value.value
        else:
            value = self.value

        return f"{color} {value}"
    
    @abstractmethod
    def is_playable(self, previous_card):
        pass

class NumberCard(Card):
    def __init__(self, color: CardColor, value: int):
        super().__init__(color)
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, entry):
        if not isinstance(entry, int) or entry not in range(10):
            raise ValueError("Each number card must have a value between 0 and 9")
        
        self._value = entry

    def is_playable(self, previous_card):
        if previous_card.color is None:
            return True
        return self.color == previous_card.color or self.value == previous_card.value

class ActionCard(Card):
    def __init__(self, color: CardColor, value: ActionCardValue):
        super().__init__(color)
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, entry):
        if not isinstance(entry, ActionCardValue):
            raise ValueError("Value must be ActionCardValue enum")
        
        self._value = entry

    def is_playable(self, previous_card):
        if previous_card.color is None:
            return True
        return self.color == previous_card.color or self.value == previous_card.value

class WildCard(Card):
    def __init__(self, value: WildCardValue):
        super().__init__(None)
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, entry):
        if not isinstance(entry, WildCardValue):
            raise ValueError("Value must be WildCardValue enum")
        
        self._value = entry
    
    def is_playable(self, previous_card):
        return True