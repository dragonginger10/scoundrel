from scoundrel.tui.weapon import WeaponSlot
from collections.abc import Generator

from loguru import logger
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widgets import Button, Digits, Log
from textual_image.widget import Image

from scoundrel.cards.card import Card, CardTypes
from scoundrel.cards.deck import Deck


class Room(HorizontalGroup):
    def __init__(self):
        self.deck: Deck = Deck()
        self.cards: int = 4
        self.deck.shuffle()
        super().__init__()

    def compose(self) -> ComposeResult:
        room: Generator[Card] = self.deck.draw(4)
        for card in room:
            logger.debug(card)
            yield CardWidget(card)
        
    def on_button_pressed(self) -> None:
        if self.cards == 1:
            self.next_room()

    def next_room(self) -> None:
        slots = self.query(CardWidget)
        required: int = sum(slot.beat for slot in slots)
        cards = self.deck.draw(required)
        for slot in slots:
            if slot.beat:
                self.cards = 4
                slot.new_card(next(cards))



class CardWidget(Container):
    DEFAULT_CSS = """
    CardWidget {
        margin: 1 0; 
        align: center middle;
    }
    CardWidget Image {
        max-width: 25;
        max-height: 20;
    }
    CardWidget Button {
        width: 100%;
        margin: 1 2;
    }
    #attack {
        display: none;
    }
    """
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
                



    def discard(self) -> None:
        room: Room = self.screen.query_one("Room", Room)
        deck: Deck = room.deck
        image = self.query_one("Image", Image)
        image.image = None
        deck.discard(self.card)
        room.cards -= 1
        self.beat = True

    def new_card(self, card: Card) -> None:
        self.card = card
        self.refresh(recompose=True)


