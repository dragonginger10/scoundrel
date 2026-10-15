from random import shuffle

from .card import *


class DeckError(Exception):
    pass

class Hand:
    def __init__(self, *args) -> None:
        self._hand: list[Card] = []
        for card in args:
            if type(card) is not Card:
                DeckError(f"{card} is not of type Card and can't be in a {self.__class__.__name__}")
            self._hand.append(card)

    def __len__(self) -> int:
        return len(self._hand)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self._hand})"

    def __str__(self) -> str:
        return f"Hand of {self.__len__()} cards" # TODO: pretty print cards

    def __iter__(self):
        return iter(self._hand)

    def __getitem__(self, index: int) -> Card:
        return self._hand[index]

    def __delitem__(self, index: int) -> None:
        del self._hand[index]

    def __add__(self, card: Card) -> None:
        self._hand.append(card)

    def shuffle(self) -> None:
        shuffle(self._hand)

    def pop(self) -> Card:
        return self._hand.pop()

    def append(self, card: Card) -> None:
        self._hand.append(card)

class Deck(Hand):
    def __init__(self) -> None:
        self._hand = [c for c in _scoundrel_cards()]
        self.shuffle()

    def draw(self, count: int = 1) -> Hand:
        if count < 1: 
            raise DeckError("Cannot draw less than one(1) card.")
        return Hand(self.pop() for _ in range(count))


def _scoundrel_cards() -> list[Card]:
    cards: list[Card] = []
    for v in CardValue:
        if v.value <= 10:
            cards.extend([Card(v, s) for s in CardSuit])
        else: 
            cards.extend([Card(v, s) for s in CardSuit if s == CardSuit.SPADES or s == CardSuit.CLUBS])
    return cards
