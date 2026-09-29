from textual.app import ComposeResult
from textual.containers import Container
from textual_image.widget import Image

from scoundrel.cards.card import Card


class WeaponSlot(Container):
    DEFAULT_CSS = """
    WeaponSlot {
      layers: below above;
      align: center middle;
    }

    #weapon {
      layer: below;
    }

    #rating {
      layer: above;
      opacity: 70%;
      offset-x: 8;
    }
    """
    def __init__(self) -> None:
        self.card: None | Card = None
        self.damage: None | Card = None
        super().__init__()

    def compose(self) -> ComposeResult:
        if self.card is None:
            yield Image()
        else:
            yield self.card.image()
            self.card.image().id = "weapon"

        if self.damage:
            self.damage.image().id = "rating"
            yield self.damage.image()

    def set_weapon(self, card: Card) -> None:
        self.card = card
        self.refresh(recompose=True)

    def attack(self, card: Card) -> None:
        self.damage = card
        self.refresh(recompose=True)
