from enum import Enum
from pathlib import Path


class CardValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
class CardSuit(Enum):
    SPADES = 1, "Monster"
    CLUBS = 2, "Monster"
    DIAMONDS = 3, "Weapon"
    HEARTS = 4, "Potion"

class CardError(Exception):
    pass

class Card:
    def __init__(self, value: CardValue, suit: CardSuit) -> None:
        self.value: CardValue = value
        self.suit: CardSuit = suit

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.value, self.suit})"
    def __str__(self) -> str:
        return f"The {self.value.name.capitalize()} of {self.suit.name.capitalize()}"

    def __le__(self, other) -> bool:
        return self.get_value() <= other.get_value()

    def __lt__(self, other) -> bool:
        return self.get_value() < other.get_value()

    def __gt__(self, other) -> bool:
        return self.get_value() > other.get_value()

    def __ge__(self, other) -> bool:
        return self.get_value() >= other.get_value()

    def __eq__(self, other) -> bool:
        return self.get_value() == other.get_value()

    def __ne__(self, other) -> bool:
        return self.get_value() != other.get_value()

    def __hash__(self):
        return hash((self.value, self.suit))

    def get_type(self) -> str:
        return self.suit.value[1]

    def code(self) -> str:
        return self.value.name[0] + self.suit.name[0]

    def image(self) -> Path:
        dir: Path = Path(__file__).parent / "images"
        return dir / f"{self.code}.png"

    def get_value(self) -> int:
        return self.value.value

    def damage(self, attack = None) -> int:
        if attack is None:
            return self.get_value()
        if attack.get_type() != "Weapon":
            raise CardError(f"Card of type {attack.get_type()} cannot be used to attak.")
        hp: int = self.get_value() - attack.get_value()
        return max(0, hp)

