from PIL.XVThumbImagePlugin import r
from textual.app import ComposeResult
from textual.containers import Container
from textual_image.widget import Image

from scoundrel.cards.card import Card, CardTypes


class WeaponSlot(Container):
    def __init__(self) -> None:
        self.weapon: None | Card = None
        self.damage: None | Card = None
        super().__init__()

    def compose(self) -> ComposeResult:
        if self.weapon is None:
            yield Image()
        else:
            yield self.weapon.image("weapon")

        if self.damage:
            yield self.damage.image("rating")

    def set_weapon(self, card: Card) -> None:
        if self.weapon is not None:
            self.discard()
        self.weapon = card
        self.refresh(recompose=True)

    def attack(self, card: Card) -> None:
        self.damage = card
        self.refresh(recompose=True)

    def has_weapon(self) -> bool:
        return self.weapon is not None

    def discard(self) -> None:
        image = self.query(Image)
        image.remove()
        
    def can_hit(self, card: Card) -> bool:
        if card.card_type != CardTypes.MONSTER:
            return False
        return self.damage is None or self.damage > card

