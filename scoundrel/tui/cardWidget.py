from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Digits
from textual_image.widget import Image

from scoundrel.cards.card import Card, CardTypes
from scoundrel.cards.deck import Deck
from scoundrel.tui.weapon import WeaponSlot


class CardWidget(Container):
    def __init__(self, card: Card, deck: Deck) -> None:
        self.card: Card | None = card
        self.deck: Deck = deck
        self.beat: bool = False
        super().__init__()

    def compose(self) -> ComposeResult:
        if self.card is not None:
            yield self.card.image()
        yield Button("Action 1", id="action")
        yield Button("Weapon", id="attack", classes="hidden")

    def on_mount(self) -> None:
        self.button_label()

    def button_label(self) -> None:
        button = self.query_one("#action", Button)
        if self.card is None:
            return
        match self.card.card_type:
            case CardTypes.MONSTER:
                button.label = "Fist"
            case CardTypes.POTION:
                button.label = "Drink"
            case CardTypes.WEAPON:
                button.label = "Use"

    @on(Button.Pressed, "#action")
    def action(self) -> None:
        new_health: int
        life: Digits = self.screen.query_one(Digits)
        health: int = int(life.value)
        if self.card is None:
            return
        match self.card.card_type:
            case CardTypes.MONSTER:
                new_health: int = health - self.card.value
                # log.write_line(f"Defeated the {self.card}!")
                self.discard()
                life.update(str(new_health))
                if new_health < 1: raise NotImplementedError("oops game over")
            case CardTypes.POTION:
                new_health: int = min(health + self.card.value, 20)
                # log.write_line(f"Restored {self.card.value} health!")
                self.discard()
                life.update(str(new_health))
            case _:
                weapon_slot: WeaponSlot = self.screen.query_one(WeaponSlot)
                weapon_slot.set_weapon(self.card)
                # log.write_line(f"Acquired a new weapon! {self.card}")
                self.discard()

                
    def discard(self) -> None:
        if self.card is None:
            return
        image = self.query_one("Image", Image)
        image.remove()
        self.beat = True
        self.deck.discard(self.card)
        self.toggle_class("hidden")
        self.card = None

    def new_card(self, card: Card) -> None:
        self.card = card
        self.beat = False
        self.remove_class("hidden")
        self.refresh()
        self.button_label()
