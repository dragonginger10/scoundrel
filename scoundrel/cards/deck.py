import random
from collections.abc import Generator

from scoundrel.cards.card import Card, Names, Suits


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = self._create_deck()
        self.discard_pile: list[Card] = []

    def __repr__(self) -> str:
        return f"Deck({len(self.cards)} of cards in deck)"

    def __len__(self) -> int:
        return len(self.cards)

    def _create_deck(self) -> list[Card]:
        cards: list[Card] = []
        for suit in Suits:
            if suit == Suits.DIAMOND or suit == Suits.HEART:
                cards.extend([Card(name, suit) for name in Names if name.value <= 10])
            else:
                cards.extend([Card(name, suit) for name in Names])

        return cards

    def _remove_cards(self) -> None:
        pass

    def _draw(self) -> Card:
        if len(self.cards) >= 1:
            return self.cards.pop()
        raise NotImplementedError

    def draw(self, count:int = 1) -> Generator[Card]:
        for _ in range(count):
            yield self._draw() 

    def shuffle(self) -> None:
        random.shuffle(self.cards)
        
    def discard(self, card: Card) -> None:
        self.discard_pile.append(card)

    def run(self, cards: list[Card]) -> Generator[Card]:
        map(self.discard, cards)
        return self.draw(4)
