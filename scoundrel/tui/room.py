from collections.abc import Generator

from loguru import logger
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widgets import Button, Digits, Log
from textual_image.widget import Image

from scoundrel.cards.card import Card, CardTypes
from scoundrel.cards.deck import Deck
from scoundrel.tui.weapon import WeaponSlot


class CardWidget(Container):
    def __init__(self, card: Card) -> None:
        self.card: Card = card
        self.beat: bool = False
        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.card.image()
        yield Button("Action 1", id="action")
        yield Button("Weapon", id="attack")

    def on_mount(self) -> None:
        button = self.query_one("#action", Button)
        match self.card.card_type:
            case CardTypes.MONSTER:
                button.label = "Fist"
            case CardTypes.POTION:
                button.label = "Drink"
            case CardTypes.WEAPON:
                button.label = "Use"

    def on_button_pressed(self) -> None:
        new_health: int
        room: Room = self.screen.query_one("Room", Room)
        digit: Digits = self.screen.query_one("#health", Digits)
        health: int = int(digit.value)
        log = self.screen.query_one("Log", Log)
        match self.card.card_type:
            case CardTypes.MONSTER:
                new_health: int = health - self.card.value
                log.write_line(f"Defeated the {self.card}!")
                self.discard()
                digit.update(str(new_health))
                if new_health < 1: raise NotImplementedError("oops game over")
            case CardTypes.POTION:
                new_health: int = min(health + self.card.value, 20)
                log.write_line(f"Restored {self.card.value} health!")
                self.discard()
                digit.update(str(new_health))
            case _:
                weapon_slot: WeaponSlot = self.screen.query_one(WeaponSlot)
                weapon_slot.set_weapon(self.card)
                log.write_line(f"Acquired a new weapon! {self.card}")
                self.discard()
                
    def discard(self) -> None:
        image = self.query_one("Image", Image)
        image.image = None
        self.beat = True

    def new_card(self, card: Card) -> None:
        self.card = card
        self.refresh(recompose=True)


