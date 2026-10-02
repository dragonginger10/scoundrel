from collections.abc import Generator

from loguru import logger
from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.css.query import DOMQuery
from textual.widgets import Button, Digits

from scoundrel.cards.deck import Card, Deck, Hand
from scoundrel.tui.room import CardWidget
from scoundrel.tui.weapon import WeaponSlot


class Scoundrel(App):

    CSS_PATH = "scoundrel.tcss"

    def __init__(self) -> None:
        self.ran: bool = False
        self.deck: Deck = Deck()
        self.life: int = 20
        self.slots: int = 4
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with HorizontalGroup(classes="game-controls"):
            yield Button("New Game")
            yield Button("Run", id="run")
            # yield Digits(self.life, id="health") TODO: Make this work with int
        room: Generator[Card] = self.deck.draw(self.slots)
        with HorizontalGroup():
            for card in room:
                logger.debug(card)
                yield CardWidget(card)

    def on_button_pressed(self) -> None:
        if self.slots == 1:
            self.next_room()

    @on(Button.Pressed, "#run")
    def runner(self) -> None:
        slots: DOMQuery[CardWidget] = self.query(CardWidget)
        cards: Hand = [c.card for c in slots]
        new_cards: Generator[Card] = self.deck.run(cards)
        for c in slots:
            c.new_card(next(new_cards))

        self.toggle_run()

    def next_room(self) -> None:
        slots: DOMQuery[CardWidget] = self.query(CardWidget)
        required: int = sum(slot.beat for slot in slots)
        cards: Generator[Card] = self.deck.draw(required)
        for slot in slots:
            if slot.beat:
                self.slots = 4
                slot.new_card(next(cards))

    def toggle_run(self) -> None:
        button: Button = self.query_one("#run", Button)
        self.ran: bool = not self.ran
        button.disabled = not button.disabled
