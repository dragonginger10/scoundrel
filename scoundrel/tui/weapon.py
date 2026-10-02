from textual.app import ComposeResult
from textual.containers import Container
from textual_image.widget import Image

from scoundrel.cards.card import Card


class WeaponSlot(Container):
    def __init__(self) -> None:
        self.card: None | Card = None
        self.damage: None | Card = None
        super().__init__()

    def compose(self) -> ComposeResult:
        if self.card is None:
            yield Image()
        else:
            yield self.card.image("weapon")

        if self.damage:
            yield self.damage.image("rating")

    def set_weapon(self, card: Card) -> None:
        self.card = card
        self.refresh(recompose=True)

    def attack(self, card: Card) -> None:
        self.damage = card
        self.refresh(recompose=True)
