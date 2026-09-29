from textual.widget import Widget
from textual.app import ComposeResult
from enum import Enum, auto
from pathlib import Path

from textual_image.widget import Image

class CardTypes(Enum):
    MONSTER = auto()
    POTION = auto()
    WEAPON = auto()


class Suits(Enum):
    HEART = auto()
    SPADE = auto()
    CLUB = auto()
    DIAMOND = auto()

    def __str__(self) -> str:
        return self.name.title()

class Names(Enum):
    ACE = 14
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

    def __str__(self) -> str:
        return self.name.title()


class Card:
    def __init__(self, name: Names, suit: Suits) -> None:
        self.card_name: Names = name
        self.suit: Suits = suit
        self.value: int = name.value
        self.card_type: CardTypes = self._get_type()
        self.back: Path = back()
        super().__init__()

    def __str__(self) -> str:
        return f"The {self.value} of {self.suit}s"

    def _get_type(self) -> CardTypes:
        match self.suit:
            case Suits.HEART: return CardTypes.POTION
            case Suits.DIAMOND: return CardTypes.WEAPON
            case _: return CardTypes.MONSTER

    def code(self) -> str:
        v = self.card_name.name[0] if self.value > 10 else str(self.value)[-1]
        s = self.suit.name[0]
        return v + s

    def image(self):
        p = Path(__file__).parent / "imgs"
        img = p / f"{self.code()}.png"

        return Image(img)


def back() -> Path:
    return Path(__file__).parent / "imgs" / "back.png"
